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

print("hello")
list1 = [1, 2, 3]
print(type(list1))
str1 = ','.join(str(e) for e in list1)
print(str1)