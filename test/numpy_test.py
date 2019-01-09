#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 10:43
# @Author  : zsj
# @File    : numpy_test.py
# @Description:
import numpy as np

from isolate_model.base_function import get_uniform_cases

# def get_uniform(num):
#     res = np.linspace(0,num,256)
#     res = [int(i) for i in res]
#     print(res)
#     print("长度：", len(res))
#
# print(get_uniform_cases(255))
# print(get_uniform_cases(200))
# print(get_uniform_cases(199))
# print(get_uniform_cases(256))
# print(get_uniform_cases(10265))

# n1 = np.array([1,3,5,7])
# n1.reshape(1,4)
# n2 = np.array([2,4,6,8])
# n2.reshape(1,4)
# n3 = np.array([9,10,11,12])
# print(np.c_[n1,n2,n3])
# n3.reshape(1,4)
# print(n1.shape)
# print(n2.shape)
# print(n3.shape)
# n4 = np.concatenate((n1,n2,n3))
# print(n4)

arr = np.arange(90).reshape((30, 3))
np.random.shuffle(arr)
print(arr)
