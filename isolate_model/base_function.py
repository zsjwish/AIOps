#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 15:11
# @Author  : zsj
# @File    : base_function.py
# @Description: 用于提供孤立森林的各种边缘功能
import numpy as np
import matplotlib.pyplot as plt

def load_csv(file_name):
    """
    使用numpy加载csv文件
    :param file_name: 要解析的csv文件名
    :return:
    """
    tmp = np.loadtxt(file_name, dtype=str, delimiter=",")
    timestamp = tmp[1:, 0]
    value = tmp[1:, 1]
    lable = tmp[1:, 2]
    kpi_id = tmp[1:, 3]
    return timestamp, value

def show_csv(timestamp, value):
    #展示数据折线图
    x_value = timestamp
    y_value = value
    plt.plot(x_value, y_value, c='r', ls='--', marker='o', lw = 1.5)
    plt.figure(figsize=(2,2))
    plt.show()