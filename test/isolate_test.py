#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 11:55
# @Author  : zsj
# @File    : isolate_test.py
# @Description:
from isolate_model.base_function import load_csv, get_uniform_cases
from isolate_model.isolate_class import Isolate


cases = load_csv("../file/big_testcase.csv")
# ##初始化模型
isolate1 = Isolate('2_7',get_uniform_cases(cases))
print(cases[0:1, :])
print(cases[0:2, :])
isolate1.judge_multy(cases[0:2, :])
