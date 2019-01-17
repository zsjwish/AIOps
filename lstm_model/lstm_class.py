#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 15:43
# @Author  : zsj
# @File    : lstm_class.py
# @Description:
import math
import time

import numpy as np
import xgboost as xgb
from keras import Sequential
from keras.layers import LSTM, Dense, Activation
from keras.losses import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from db.mysql_operation import insert_xgboost_model, update_xgboost_model
from isolate_model.base_function import load_data_for_lstm_from_mysql


class LSTMModel:
    def __init__(self, model_name):
        self.name = model_name
        # 预测需要前面多少值
        self.look_back = 30
        # 最后预测时间
        self.lasted_predict = None
        # 最后预测的值,str拼接起来
        self.predict_value = None
        # 训练集测试集比例
        self.rate = [7, 3]
        # 模型初始化时间
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 模型最后更新时间
        self.lasted_update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 均方根误差，用来判断模型预测效果
        self.rmse = 0
        self.model = self.init_model()

    def init_model(self):
        # 从数据库获取数据，model_name就是表名,最后截止时间是创建表的时间，数据为一天的数据量
        data = load_data_for_lstm_from_mysql(self.name, self.create_time, 7)
        data = data.reshape(len(data), 1)
        # 归一化处理
        scaler = MinMaxScaler(feature_range = (0, 1))
        data = scaler.fit_transform(data)

        train_size = int(sum(self.rate) * self.rate[0])
        train, test = data[0:train_size, :], data[train_size:len(data), :]

        trainX, trainY = create_dataset(train)
        testX, testY = create_dataset(test)
        # 转换成三维输入，sample，time step，feature
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        # 初始化模型，train_x的维度为(n_samples, time_steps, input_dim)
        model = Sequential()
        # 增加LSTM网络层
        model.add(LSTM(50, input_shape = (1, look_back), return_sequences = True))
        model.add(LSTM(100, return_sequences = False))
        model.add(Dense(units = 1))
        model.add(Activation('linear'))
        model.compile(loss = 'mse', optimizer = 'rmsprop')
        # 模型训练
        model.fit(trainX, trainY, epochs = 100, batch_size = 5, verbose = 2)
        # 预测训练数据
        trainPredict = model.predict(trainX)
        # 预测测试数据
        testPredict = model.predict(testX)
        # 将标准化后是数据转换为原始数据
        trainPredict = scaler.inverse_transform(trainPredict)
        trainY = scaler.inverse_transform([trainY])
        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])
        trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
        print('Train Score: %.2f RMSE' % (trainScore))
        testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
        print('Test Score: %.2f RMSE' % (testScore))
        self.rmse = min(trainScore, testScore)
        self.model = model
        return model

    def create_dataset(self, dataset):
        """
        对从数据库获取的数据进行处理，变成特征x和y的形式
        :param dataset:
        :return:
        """
        look_back = self.look_back
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back):
            a = dataset[i:(i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        print("dataX", dataX)
        print("dataY", dataY)
        return np.array(dataX), np.array(dataY)

    def predict(self):
        """
        对格式化后的数据进行预测，如果判断为异常则返回1，判断正常则返回0
        :param data: 格式化后的数据，即时间已转换成星期，小时，分钟，没有label，
        :return: 异常1， 正常0
        """
        data = load_data_for_lstm_from_mysql(self.name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 1)
        data = data.reshape(len(data), 1)
        # 归一化处理
        scaler = MinMaxScaler(feature_range = (0, 1))
        data = scaler.fit_transform(data)

        self.model.predict()
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


def create_dataset(dataset):
    """
        对从数据库获取的数据进行处理，变成特征x和y的形式
        :param dataset:
        :return:
        """
    look_back = 5
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    print("dataX", dataX)
    print("dataY", dataY)
    return np.array(dataX), np.array(dataY)

np.random.seed(7)
look_back = 5
data = np.array(range(100))
data = data.reshape(len(data), 1)
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)
print(type(data))
print(data)
train_size = int(len(data) * 0.70)
test_size = len(data) - train_size
train, test = data[0:train_size, :], data[train_size:len(data), :]

trainX, trainY = create_dataset(train)
testX, testY = create_dataset(test)
# 转换成三维输入，sample，time step，feature
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

model = Sequential()
model.add(LSTM(50, input_shape = (1, look_back), return_sequences = True))
model.add(LSTM(100, return_sequences = False))
model.add(Dense(units = 1))
model.add(Activation('linear'))
model.compile(loss = 'mse', optimizer = 'rmsprop')
model.fit(trainX, trainY, epochs=100, batch_size = 5, verbose = 2)

print(len(trainX))
testPredict = model.predict(testX)
print(testX)
print(len(testX))
testPredict = scaler.inverse_transform(testPredict)
print(testPredict)
print(len(testPredict))