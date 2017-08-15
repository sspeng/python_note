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

sess.close()