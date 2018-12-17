#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 11:55
# @Author  : zsj
# @File    : isolate_test.py
# @Description:
from isolate_model.base_function import load_csv
from isolate_model.isolate_class import Isolate


cases = load_csv("../file/csv_test.csv")
isolate1 = Isolate(cases)
isolate1.init_model()