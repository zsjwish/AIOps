#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 16:14
# @Author  : zsj
# @File    : array_test.py
# @Description:
import csv

from isolate_model.base_function import load_csv, show_csv, get_uniform_cases
import pandas as pd
import numpy as np
# res = load_csv("../file/csv_test1.csv")
# print(res)
# show_csv(res, 1, 2)
# show_csv(res, 1, 3)
# l = np.arange(0,20)
# print(l)
# l.astype(np.float16)
# print(l)

# a = list(range(20))
# a = [str(i) for i in a]
# print(a)
# x = np.array(['1','2','3'],dtype = np.string_)
# print(x)


data=load_csv("../file/csv_total1.csv")
data1 = get_uniform_cases(data)
print(data1)
show_csv(data1, 1, 2)
show_csv(data1, 1, 3)

