#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:35
# @Author  : zsj
# @File    : xgboost_class.py
# @Description:
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
        # 准确率
        self.accuracy = 0.
        # 召回率
        self.recall = 0.

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

    def train_model(self):
        # 训练模型并使用验证集验证
        bst = xgb.train(self.param, self.dtrain, self.num_round, self.watchlist)
        # 预测测试集数据
        preds = bst.predict(self.dtest)
        # 原本测试集的label
        labels = self.dtest.get_label()
        accuraty = 0

        for i, label in enumerate(labels):
            if int(preds[i]) != label:
                pass
                # 得出精确率和召回率
        print('error=%f' % (sum(1 for i in range(len(preds)) if int(preds[i] > 0.5) != labels[i]) / float(len(preds))))
        return bst

    def predict(self, data):
        pass

    def insert_database(self):

    def save_model(self):
        pass

    def load_mode(self):
        pass
