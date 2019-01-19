#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 17:06
# @Author  : zsj
# @File    : lstm_test2.py
# @Description:
# load the dataset

import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

dataframe = read_csv('international-airline-passengers.csv', usecols=[1], engine='python', skipfooter=3)
dataset = dataframe.values
# 将整型变为float
dataset = dataset.astype('float32')

plt.plot(dataset)
plt.show()


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=3):
    dataX, dataY = [], []
    print(type(dataset))
    print(dataset.shape)
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)


# fix random seed for reproducibility
numpy.random.seed(7)

# 归一化处理，范围在0~1之内
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

print(dataset.shape)
print(type(dataset))
# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

look_back = 3
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
print(trainX.shape)
# 将2维 sample和feature转换成三维(sample, time step, feature)
trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
print(trainX.shape)
testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))

# 初始化模型
model = Sequential()
# 添加LSTM模型
model.add(LSTM(50, input_shape=(look_back, 1)))
# 添加核心网络层
model.add(Dense(1))
# 配置训练模型，loss损失函数
model.compile(loss='mean_squared_error', optimizer='adam')
print(trainX.shape)
# 训练模型 x:样本，y:标签，epochs训练轮数，verbose:输出信息(0=无，1=进度条，2=每个时期一行),batch_size:并行数，默认32
model.fit(trainX, trainY, epochs=100, batch_size = 5, verbose = 2)

trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test Score: %.2f RMSE' % (testScore))

trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()
