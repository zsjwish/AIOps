#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 10:43
# @Author  : zsj
# @File    : numpy_test.py
# @Description:
import numpy as np

from isolate_model.base_function import get_uniform_cases


def get_uniform(num):
    res = np.linspace(0,num,256)
    res = [int(i) for i in res]
    print(res)
    print("长度：", len(res))

print(get_uniform_cases(255))
print(get_uniform_cases(200))
print(get_uniform_cases(199))
print(get_uniform_cases(256))
print(get_uniform_cases(10265))
