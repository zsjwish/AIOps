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

data=load_csv("../file/big_testcase.csv")
data1 = get_uniform_cases(data)
print(data1)
show_csv(data1, 1, 2)
show_csv(data1, 1, 3)

