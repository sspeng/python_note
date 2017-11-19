#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:39:32 2017

@author: manout
"""

import numpy as np
import time

a = np.array([1, 2, 3, 4])
print(a)

a = np.random.rand(1000000)
b = np.random.rand(1000000)
print(a)
tic = time.time()
c = np.dot(a, b)
toc = time.time()
print(c)
print("Vectorized version: " + str(1000 * (toc - tic)) + "ms")

c = 0
tic = time.time()

for i in range(1000000):
    c += a[i] * b[i]

toc = time.time()

print(c)
print("For loop: version: " + str(1000 * (toc - tic)) + "ms")
