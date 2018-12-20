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
    使用numpy加载csv文件,并把除了host_id的都转换成float类型，因为孤立森林只能判别数值类型
    csv文件的格式是： host_id(主机群和主机标识), timestamp, kpi_1, kpi_2, kpi_3, kpi_4.....
    :param file_name: 要解析的csv文件名
    :return:
    """
    array = np.loadtxt(file_name, dtype=str, delimiter=",", encoding='utf-8')
    return array

def show_csv(array, array_x, array_y):
    """
    将读取的csv文件中某两列取出来作为图形展示的x轴和y轴
    :param array:转置后的数组
    :param array_x:数组第x列,一般来说x轴是时间
    :param array_y:同上
    :return:
    """
    #从第三个值开始取，因为第一个是host_id,第二个是时间戳
    x_value = array[1:, array_x]
    y_value = array[1:, array_y]
    #获取label标签，知道是那两行作图
    label_x = array[0, array_x]
    label_y = array[0, array_y]
    if "timestamp" in label_x:
        #一般来说x轴都是时间戳
        x_value = [timestamp_to_time(x) for x in x_value]
    else:
        x_value = [float(x) for x in x_value]
    y_value = [float(y) for y in y_value]
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

def get_uniform_cases(arrays, size=257):
    """
    由于传入的测试集不可能刚好是256个，所以需要均匀取周期内的256个case作为测试集
    仅仅用于训练模型时使用
    :param arrays:测试集数组
    :param size:int, 要求均匀分为的份额，一般为256，用户可以自己设置,第一行为标签
    :return:
    """
    length = len(arrays)
    if length < 200:
        print("测试集大小：", length)
        return "测试集数据小于200，请重新传入大于200条数据的测试集"
    elif length < 256:
        print("测试集大小：", length)
        return arrays
    indexs = np.linspace(0, length-1, size)
    indexs = np.array(indexs, dtype=int)
    res_arr = arrays[indexs]
    print("测试集大小：", len(indexs)-1)
    return res_arr

