#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:35
# @Author  : zsj
# @File    : xgboost_class.py
# @Description:
import time

import numpy as np
import xgboost as xgb


class Xgboost:
    def __init__(self, model_name, datas):
        self.name = model_name
        self.param = {
            'booster': 'gbtree',  # 助推器，默认为gbtree，可不写
            'verbosity': 0,  # verbosity：1警告信息
            'objective': 'binary:logistic',  # objective：binary：logistic 二分类逻辑回归，输出概率
            'max_depth': 10,  # 最大深度，默认为6
            'eta': 0.05,  # eta 步长
            'subsample': 0.9,  # 每次取0.9比例的样本，防止过拟合
            'evals': 'auc'
        }
        # 决策树的颗数
        self.num_round = 10
        # 精确率
        self.precision = 0.
        # 召回率
        self.recall = 0.
        # F1值
        self.f1 = 0.
        # 按行打乱顺序，然后从中选择训练集，测试集, 验证集
        np.random.shuffle(datas)
        self.datas = datas
        # 训练集和测试集取9:1，用于取准备率和召回率
        self.rate = [9, 1]
        # 总比例，用于取出训练集和测试集
        total_rate = sum(self.rate)
        self.number_datas = len(self.datas)
        rate_num1 = int(self.number_datas * self.rate[0] / total_rate)
        # 训练集
        self.dtrain = xgb.DMatrix(self.datas[0:rate_num1, 1:-1].astype(float),
                                  label = self.datas[0: rate_num1, -1].astype(int))
        # 测试集
        self.dtest = xgb.DMatrix(self.datas[rate_num1 + 1: -1, 1:-1].astype(float),
                                 label = self.datas[rate_num1 + 1: -1, -1].astype(int))
        # 显示训练过程
        self.watchlist = [(self.dtrain, 'train'), (self.dtest, 'test')]
        # 模型初始化时间
        self.create_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    def train_model(self):
        # 训练模型并使用验证集验证
        bst = xgb.train(self.param, self.dtrain, self.num_round, self.watchlist)
        # 预测测试集数据
        preds = bst.predict(self.dtest)
        # 原本测试集的label
        labels = self.dtest.get_label()
        # 真实为1，预测为1
        TP = 0
        # 真实为1，预测为0
        FN = 0
        # 真实为0，预测为1
        FP = 0
        for i, label in enumerate(labels):
            if preds[i] >= 0.5:
                if label == 1:
                    TP += 1
                else:
                    FP += 1
            elif label == 1:
                FN += 1
        # 得出精确率和召回率
        self.precision = TP / float(TP + FP)
        self.recall = TP / float(TP + FN)
        self.f1 = self.precision * self.recall * 2 / float(self.precision + self.recall)
        return bst

    def predict(self, data):
        pass

    def insert_database(self):
        pass

    def save_model(self):
        pass

    def load_mode(self):
        pass
