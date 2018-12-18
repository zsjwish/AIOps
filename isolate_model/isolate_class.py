#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/16 17:19
# @Author  : zsj
# @File    : isolate_class.py
# @Description:
import numpy as np
from sklearn.ensemble import IsolationForest


class Isolate():
    def __init__(self, name, test_cases, cases_size=256, rate=0.1):
        """
        初始化孤立森林
        :param test_cases: 测试集
        :param cases_size: 测试集大小，默认为256
        :param rate: 异常比例，默认为0.1
        """
        #模型的标志，每个模型名字独一无二
        self.name = name
        self.test_cases = test_cases
        #数据集第一行，返回的时候对应返回
        self.title = test_cases[0, 1:]
        # print("title:", self.title)
        #数据集第一列，host_id
        self.host = test_cases[:, 0]
        # print("host_id:", self.host)
        #数据集真实数据
        self.cases = test_cases[1:, 1:].astype(np.float64)
        # print("cases:", self.cases)
        #定义测试集大小，默认为256
        self.cases_size = cases_size
        #定义测试集异常比例，默认为0.1
        self.rate = rate
        #随机因子
        self.rng = np.random.RandomState()
        #初始化模型，如果模型要更改就直接在该函数中修改
        self.clf = IsolationForest(behaviour='new', max_samples=self.cases_size,
                              random_state=self.rng, contamination=self.rate)
        self.init_model()

    def init_model(self):
        #初始化模型、训练及大小，异常数据比例
        #训练数据
        self.clf.fit(self.cases)
        print('-------训练完成--------')
        self.judge_multy(self.test_cases)

    def judge_multy(self, datas):
        """
        判断批量数据是否是异常数据，返回异常数据集合，如果没有异常返回true
        datas：数据集合
        """
        #获取异常检测结果，存放在list中
        multy_res = self.clf.predict(datas[1:, 1:].astype(np.float64))
        #如果list中没有-1，则返回True
        if sum(multy_res == -1) == 0:
            return True, None
        #否则首先获取到异常集大小
        abnormal_size = sum(multy_res == -1)
        #重新整理host_id
        res_host_id = datas[:abnormal_size+1, 0].reshape(abnormal_size+1,1)
        #整理异常数据集
        res_cases = datas[1:, 1:]
        res_cases = res_cases[multy_res == -1]
        #整理title
        res_title = datas[0, 1:].reshape(1,4)
        #拼接title和异常数据集
        res_tmp = np.concatenate((res_title, res_cases), axis=0)
        #拼接title，异常数据集，host_id
        res = np.concatenate((res_host_id, res_tmp), axis = 1)
        #返回False，异常数据集
        print("--------异常检测完成-------")
        print("--------异常数据：---------")
        print(res)
        return False, res



    def get_data(self,time_start, time_end, condition):
        """
        按条件查询某时间段内的数据,需要数据库
        :param time_start:
        :param time_end:
        :param condition:
        :return:
        """
        pass