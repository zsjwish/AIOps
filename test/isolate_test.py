#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 11:55
# @Author  : zsj
# @File    : isolate_test.py
# @Description:
from isolate_model.base_function import load_csv, get_uniform_cases, show_csv
from isolate_model.isolate_class import Isolate


cases = load_csv("../file/customs_test1.csv")

# ##初始化模型
isolate1 = Isolate('2_7',cases)
# isolate1.init_model()

show_csv(cases, 1, 2)
