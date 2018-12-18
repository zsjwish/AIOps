#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 17:10
# @Author  : zsj
# @File    : array_test2.py
# @Description:
import numpy as np

arr = np.arange(12).reshape(3,4)
a1 = arr.astype(str)
print(a1)
for i in range(3):
    for j in range(4):
        a1[i,j] = str(100+i+j)+'f'
print(a1)

print(str(2*3)+'d')