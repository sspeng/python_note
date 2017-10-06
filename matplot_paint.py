#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0, 10, 1000)
y = np.sin(x) + 1
z = np.cos(x ** 2) + 1

plt.figure(figsize=(8, 4))
plt.plot(x, y, label='$\sin x+1$', color='red', linewidth=2)
plt.plot(x, z, 'b--', label='$\cos x^2+1$')
plt.xlabel('Time(s) ')
plt.ylabel('Volt')
plt.title('A Simple Example')
plt.ylim(0, 2.2)
plt.legend()
plt.show()
