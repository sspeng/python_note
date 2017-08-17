#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:53:22 2017

@author: manout
"""

import input_data
import tensorflow as tf

# load MNist data set 
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# build compute graph 
sess = tf.InteractiveSession()


# build regression model
# x and y_ are just placeholder
# x is a 2 dimension tenosr, the second dimension represents the dimension 
# of the flatten MNIST image
# the None means the first dimensions is not sure
x = tf.placeholder("float", shape=[None, 784])

# y_ is a 2 dimension tensor, which represents the category of one image
y_ = tf.placeholder("float", shape=[None, 10])


# model parameter Weight and bias
# all initialize with 0
W = tf.Variable(tf.zeros([784, 10]))

b = tf.Variable(tf.zeros([10]))

# variable need to be initialize with session so that it can be used in session
sess.run(tf.global_variables_initializer())

# implement regression model with just one line
# vectoring image times weight matrix then plus bias
# then compute the softmax probability of each category
y = tf.nn.softmax(tf.matmul(x, W) + b)

# defien loss function 
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

# use strrpest descent method to to decrease cross entropy, step size is 0.01
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# the training of the model can be complete though run train_step repeatedly
for i in range(1000):
    batch = mnist.train.next_batch(50)
    train_step.run(feed_dict={x:batch[0], y_:batch[1]})

# evaluate the perfornabce of our model, this line returns a bool array 
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

# evaluate the accuracy, sum the bool array and divide by its length
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# compute the accuracy of our result base on the test data, its about 91%
print(accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels}))


"""
    build multilayer convolve network
"""

""" 
    init weight and bias
"""
# weight need add some noise when its initialize to break summetry 
# and zero gradient
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

# since we use ReLU unit, initialize bias with a small positive number 
# is a better way, in order to avoid nerve unit outputs zero all the time  
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
"""
    convolve and pooling
"""

# our convolve use 1 stepsize, 0 padding size template, promise output is the 
# same size of the output
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], 
                          strides=[1, 2, 2, 1], padding='SAME')

"""
    first convolve layer
"""
 
# here to implement the first convolve layer
# it is accomplish by conbolve and maxpooling
# the shape of convlove weight tensor is [5, 5, 1, 32], the first two dimension 
# is the size of the batch, then the count of input channels, the last is the 
# count of output channels. Each output channel is correspond to a bias
W_conv1 = weight_variable([5, 5, 1, 32])

b_conv1 = bias_variable([32])


# we change x into a 4 dimension vector. The 2th, 3th correspond to the height
# and width of the picture, the last dimension represent the number of 
# image color channel 
x_image = tf.reshape(x, shape=[-1, 28, 28, 1])

# we then convlove x_image with the weight tensor, add the bias, apply the ReLU
# function, and finally max pooling
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

h_pool1 = max_pool_2x2(h_conv1)

"""
    second convlove layer
"""

# in order to get a deeper network, we can pile some similar layers
# in the second layer, every patch will get 64  features
W_conv2 = weight_variable([5, 5, 32, 64])

b_conv2 = bias_variable([64])


"""
    dense connect layer
"""

# the size of iamge shrink into 7 x 7, we add a all connectivity layer to 
# process the entire image. we reshape the tensor ouput by max pooling layer 
# into some vector, mutiply weight matrix, add bias, the apply ReLU on it
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])

b_fc1 = bias_variable([1024])


h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

"""
    dropout
"""

# inorder to reduce overfitting, we add dropout before output layer
# we use a placeholder to represent the probability the output of nerve unit 
# remain unchanged in dropout. we apply dropout in the train, and shutdown 
# dropout in the testing
# the tf.nn.dropout in tensorflow not only can shield the output of a nerve unit
# but also can process the scale of the nerve unit output automaticly
# so we don't need to consider scale when we use dropout
keep_prob = tf.placeholder("float")

h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


"""
    output layer 
"""

# finally we add a softmax layer, just like the single softmax regrssion layer
# we add before
W_fc2 = weight_variable([1024, 10])

b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

"""
    train and evaluate model
"""

# the code we use is about the same as the simple single layer softmax nerve 
# network model we use before, but we use the more complex ADAM optimizer
# to do gradient of steepest descent, add extra parameter in feed_dict to 
# control the percentge of dropout
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

sess.run(tf.global_variables_initializer())

for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
                                        x:batch[0], y_:batch[1], 
                                        keep_prob: 1.0})
        print("step %d, train accucary %g"%(i,train_accuracy))
    train_step.run(feed_dict={x:batch[0], y_:batch[1], keep_prob: 0.5})

# the total accuracy is about 99.2% 
print("test accuracy %g"%(accuracy.eval(feed_dict={
                        x:mnist.test.images, y_: mnist.test.labels, 
                        keep_prob:1.0})))















