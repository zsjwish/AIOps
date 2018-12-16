#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 16:14
# @Author  : zsj
# @File    : array_test.py
# @Description:
from isolate_model.base_function import load_csv, show_csv

array1 = list(range(10))
array2 = list(range(11,20))
print(array1)
print(array2)
array3 = [array1, array2]
print(array3)
print(array3[1][3])

res = load_csv("../file/csv_test.csv")
print(res)
show_csv(res, 0, 1)
show_csv(res, 0, 2)