#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 15:11
# @Author  : zsj
# @File    : base_function.py
# @Description: 用于提供孤立森林的各种边缘功能
import time

import numpy as np
import matplotlib.pyplot as plt

def load_csv(file_name):
    """
    使用numpy加载csv文件
    csv文件的格式是： timestamp, 主机群和主机标识， KPI1, KPI2, KPI3, KPI4.....
    :param file_name: 要解析的csv文件名
    :return:
    """
    array = np.loadtxt(file_name, dtype=str, delimiter=",", encoding='utf-8')
    return array.T

def show_csv(array, array_x, array_y):
    """
    将读取的csv文件中某两列取出来作为图形展示的x轴和y轴
    :param array:转置后的数组
    :param array_x:数组第x行，也就是转置前第x列,一般来说x轴是时间
    :param array_y:同上
    :return:
    """
    #从第二个值开始取，因为第一个是label
    x_value = array[array_x][1:]
    y_value = array[array_y][1:]
    #获取label标签，知道是那两行作图
    label_x = array[array_x][0]
    label_y = array[array_y][0]
    if "timestamp" in label_x:
        #一般来说x轴都是时间戳
        x_value = [timestamp_to_time(x) for x in x_value]
    else:
        x_value = [float(x) for x in x_value]
    y_value = [float(t) for t in y_value]
    plt.plot(x_value, y_value, c='r', ls='--', marker='o', lw = 1.5, label=label_x)
    plt.xticks(range(0, len(x_value), 3), rotation=90)
    # plt.figure(dpi=128, figsize=(10, 6))
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()


def timestamp_to_time(timestamp):
    """
    单个时间戳转换成时间，格式为2018-12-14 19:00:00
    :param timestamp:
    :return:
    """
    timestamp = int(timestamp)
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d: %H:%M:%S", time_local)

def simplify_timestamp(timestamps):
    """
    时间戳批量转换成时间
    :param timestamps: 时间戳list
    :return:
    """
    return [timestamp_to_time(timestamp) for timestamp in timestamps]

def get_uniform_cases(total, uniform_cases=256):
    """
    由于传入的测试集不可能刚好是256个，所以需要均匀取周期内的256个case作为测试集
    :param total:int, 测试集总大小
    :param uniform_cases:int, 要求均匀分为的份额，一般为256，用户可以自己设置
    :return:
    """
    if total < 200:
        print("测试集大小：", total)
        return "测试集数据小于200，请重新传入大于200条数据的测试集"
    elif total < 256:
        print("测试集大小：", total)
        return list(range(total))
    res = np.linspace(0, total, uniform_cases)
    res = [int(i) for i in res]
    print("测试集大小：", len(res))
    return res