#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:35
# @Author  : zsj
# @File    : xgboost_class.py
# @Description:
import time

import numpy as np
import xgboost as xgb

from db.mysql_operation import insert_xgboost_model
from isolate_model.base_function import load_data_from_mysql


class Xgboost:
    def __init__(self, model_name):
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
        # 测试集总数量，训练总数量
        self.trained_number = 0
        # 是否训练完成,0未完成，1完成
        self.finished = 0
        # 模型最近是否发生了改变,0未改变，1已改变，需要重新训练
        self.changed = 0
        # 模型初始化时间
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 模型最后更新时间
        self.lasted_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 初始化模型
        self.model = self.init_model()

    def init_model(self):
        # 从数据库获取数据，model_name就是表名
        datas = load_data_from_mysql(self.name)
        # 按行打乱顺序，然后从中选择训练集，测试集, 验证集
        np.random.shuffle(datas)
        # 训练集和测试集取9:1，用于取准备率和召回率
        rate = [9, 1]
        # 训练集总数量
        self.trained_number = len(datas)
        # 总比例，用于取出训练集和测试集
        total_rate = sum(rate)
        rate_num1 = int(self.trained_number * rate[0] / total_rate)
        # 训练集
        dtrain = xgb.DMatrix(datas[0:rate_num1, 1:-1].astype(float),
                             label = datas[0: rate_num1, -1].astype(int))
        # 测试集
        dtest = xgb.DMatrix(datas[rate_num1 + 1: -1, 1:-1].astype(float),
                            label = datas[rate_num1 + 1: -1, -1].astype(int))
        # 训练模型并使用验证集验证
        # 显示训练过程
        watchlist = [(dtrain, 'train'), (dtest, 'test')]
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
        for i, label in enumerate(labels):
            if preds[i] >= 0.5:
                if label == 1:
                    TP += 1
                else:
                    FP += 1
            elif label == 1:
                FN += 1
        print("TP", TP)
        print("FN", FN)
        print("FP", FP)
        print("lenght", len(labels))
        # 得出精确率、召回率和F1
        self.precision = TP / float(TP + FP)
        self.recall = TP / float(TP + FN)
        self.f1 = self.precision * self.recall * 2 / float(self.precision + self.recall)
        self.lasted_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 更新模型
        self.model = bst
        # 返回模型
        # 插入数据库
        self.insert_database()
        return bst

    def predict(self, data):
        pass

    def insert_database(self):
        if insert_xgboost_model(self.name, self.precision, self.recall,
                             self.f1, self.trained_number, self.finished,
                             self.changed, self.create_time, self.lasted_update):
            print("插入成功")

    def save_model(self):
        pass

    def load_mode(self):
        pass
