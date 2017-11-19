#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

R = 3
W = 10

X = np.linspace(0, 10,1000, endpoint=True)

C, S = np.sin(W * X) + R, np.cos(W * X) + R

ax1 = plt.subplot(111, projection='polar')
ax1.plot(X, C)
plt.show()
