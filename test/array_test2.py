#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 17:10
# @Author  : zsj
# @File    : array_test2.py
# @Description:
import numpy as np

list = np.arange(0,20).reshape(2,10)
print(list)
list[1][3] = '123'
print(list[1][3])
print(type(list[1][3]))
list3 = list[0]
list2 = list[1].astype(np.string_)
print(list2)
l = np.r_[list3, list2]
print(l)
print(list2.dtype)