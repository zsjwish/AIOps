#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/16 17:19
# @Author  : zsj
# @File    : isolate_class.py
# @Description:
import numpy as np
from sklearn.ensemble import IsolationForest


class Isolate():
    def __init__(self, test_cases, cases_size=256, rate=0.1):
        """
        初始化孤立森林
        :param test_cases: 测试集
        :param cases_size: 测试集大小，默认为256
        :param rate: 异常比例，默认为0.1
        """
        self.test_cases = test_cases
        self.cases_size = cases_size
        self.rate = rate
        self.rng = np.random.RandomState()

    def init_model(self):

        clf = IsolationForest(behaviour='new', max_samples=self.cases_size,
                              random_state=self.rng, contamination=self.rate)
        size = len(self.test_cases)
        title = self.test_cases[:][0]
        cases = self.test_cases[0][1:]
        for i in range(size-1):
            tmp = [float(case)for case in self.test_cases[i+1][1:]]
            cases = np.c_(cases, tmp)
        print(title)
        print(cases)


    def judge_single(self,data):
        pass

    def judge_multy(self, datas):
        pass

    def get_data(self,time_start, time_end, condition):
        pass