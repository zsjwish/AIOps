#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 16:14
# @Author  : zsj
# @File    : array_test.py
# @Description:
import csv

from isolate_model.base_function import load_csv, show_csv
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


data=csv.reader(open('../file/csv_test1.csv'))
res = []
for row in data:
    res.append(row)
print(res)
print(type(res[2][2]))
print(res[2][2])
print(res[3])
print("res:", res[1:][1:1])
for i in res[1:][1]:
    print(i)
res[1:][1] = [int(i) for i in res[1:][1]]
print(res)
print(type(data))
