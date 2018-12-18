#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 17:10
# @Author  : zsj
# @File    : array_test2.py
# @Description:
import numpy as np

n1 = np.arange(20).reshape(5,4)
n4 = n1[[1,3]]
print(n4)
n2 = np.arange(20,24).reshape(1,4)
n3 = np.concatenate((n1, n2),axis=0)
print(n3)

