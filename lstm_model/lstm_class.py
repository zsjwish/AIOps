#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 15:43
# @Author  : zsj
# @File    : lstm_class.py
# @Description:

import time
import numpy as np
import xgboost as xgb

from db.mysql_operation import insert_xgboost_model, update_xgboost_model
from isolate_model.base_function import load_data_for_xgboost_from_mysql


class LSTM:
    def __init__(self, model_name):
        self.name = model_name
        # 预测需要前面多少值
        self.look_back = 30
        # 最后预测时间
        self.lasted_predict = None
        # 最后预测的值,str拼接起来
        self.predict_value = None
        # 模型初始化时间
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 模型最后更新时间
        self.lasted_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def init_model(self):
        # 从数据库获取数据，model_name就是表名
        datas = load_data_for_xgboost_from_mysql(self.name)
        # 按行打乱顺序，然后从中选择训练集，测试集, 验证集
        np.random.shuffle(datas)
        # 训练集和测试集取9:1，用于取准备率和召回率
        rate = [7, 3]
        # 训练集总数量
        self.trained_number = len(datas)
        # 总比例，用于取出训练集和测试集
        total_rate = sum(rate)
        rate_num1 = int(self.trained_number * rate[0] / total_rate)
        # 训练集
        print(datas)
        dtrain = xgb.DMatrix(datas[0:rate_num1, 0:-1].astype(float),
                             label = datas[0: rate_num1, -1].astype(int))
        # 验证集
        dtest = xgb.DMatrix(datas[rate_num1 + 1: -1, 0:-1].astype(float),
                            label = datas[rate_num1 + 1: -1, -1].astype(int))
        # 显示训练过程
        watchlist = [(dtrain, 'train'), (dtest, 'test')]
        # 训练模型并使用验证集验证
        bst = xgb.train(self.param, dtrain, self.num_round, watchlist)
        # 预测测试集数据
        preds = bst.predict(dtest)
        # 原本测试集的label
        labels = dtest.get_label()
        # 真实为1，预测为1
        TP = 0
        # 真实为1，预测为0
        FN = 0
        # 真实为0，预测为1
        FP = 0
        # 真实为0，预测为0
        TN = 0
        p = []
        for i, label in enumerate(labels):
            p.append(int(preds[i] + 0.5))
            if preds[i] >= 0.5:
                if label == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if label == 1:
                    FN += 1
                else:
                    TN += 1
        print("TP", TP)
        print("FN", FN)
        print("FP", FP)
        print("TN", TN)
        # 得出精确率、召回率和F1
        self.precision = TP / float(TP + FP)
        self.recall = TP / float(TP + FN)
        self.f1 = self.precision * self.recall * 2 / float(self.precision + self.recall)
        self.lasted_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 更新模型
        self.model = bst
        # 更新数据库
        self.update_database_model()
        # 返回模型
        return bst

    def predict(self, data):
        """
        对格式化后的数据进行预测，如果判断为异常则返回1，判断正常则返回0
        :param data: 格式化后的数据，即时间已转换成星期，小时，分钟，没有label，
        :return: 异常1， 正常0
        """
        return int(self.model.predict(xgb.DMatrix(data)) + 0.5)

    def insert_database_model(self):
        """
        插入数据到model表中，初始化的时候会插入数据，后续都是update
        :return:插入成功，返回True,失败返回False
        """
        if insert_xgboost_model(self.name, self.precision, self.recall,
                                self.f1, self.trained_number, self.finished,
                                self.changed, self.create_time, self.lasted_update):
            print("插入成功")
            return True
        return False

    def update_database_model(self):
        """
        重新训练数据后会更新，只更新数据
        :return:
        """
        if update_xgboost_model(self.name, self.precision, self.recall,
                                self.f1, self.trained_number, self.finished,
                                self.changed, self.lasted_update):
            print("更新成功")
            return True
        return False
