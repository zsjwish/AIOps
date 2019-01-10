#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 15:11
# @Author  : zsj
# @File    : base_function.py
# @Description: 用于提供孤立森林的各种边缘功能

import re
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from isolate_model.isolate_class import Isolate


def load_csv(file_name):
    """
    使用numpy加载csv文件,并把除了host_id的都转换成float类型，因为孤立森林只能判别数值类型
    csv文件的格式是： host_id(主机群和主机标识), timestamp, kpi_1, kpi_2, kpi_3, kpi_4.....
    :param file_name: 要解析的csv文件名
    :return:
    """
    array = np.loadtxt(file_name, dtype = str, delimiter = ",", encoding = 'utf-8')
    return array


def show_csv(array, array_x, array_y):
    """
    将读取的csv文件中某两列取出来作为图形展示的x轴和y轴
    :param array:转置后的数组
    :param array_x:数组第x列,一般来说x轴是时间
    :param array_y:同上
    :return:
    """
    # 从第三个值开始取，因为第一个是host_id,第二个是时间戳
    x_value = array[1:, array_x]
    y_value = array[1:, array_y]
    # 获取label标签，知道是那两行作图
    label_x = array[0, array_x]
    label_y = array[0, array_y]
    if "timestamp" in label_x:
        # 一般来说x轴都是时间戳
        # x_value = [format_time(x) for x in x_value]
        x_value = [x for x in x_value]
    else:
        x_value = [float(x) for x in x_value]
    y_value = [float(y) for y in y_value]
    plt.plot(x_value, y_value, c = 'r', ls = '--', marker = 'o', lw = 1.5, label = label_x)
    plt.xticks(range(0, len(x_value), int(len(x_value) / 30)), rotation = 90)
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
    indexs = np.linspace(0, length - 1, size)
    indexs = np.array(indexs, dtype = int)
    res_arr = arrays[indexs]
    print("测试集大小：", len(indexs) - 1)
    return res_arr


def format_time(time):
    """
    将传入的时间格式化，转换成没有秒的时间格式 yyyy-MM-DD hh-mm
    :param time:
    :return:
    """
    # year, month, day, hour, minute, scend = re.split(r"/| |:", time)
    # print(year, month, day, hour, minute, scend)
    return time[0:-3]


def draw_with_diff_color(np_array):
    """
    根据标签展示散点图，不同的标签具有不同颜色
    :param np_array:
    :return:
    """
    red_arr = []
    green_arr = []
    for arr in np_array:
        if arr[-1] == '0':
            red_arr.append(arr)
        else:
            green_arr.append(arr)
    print(red_arr)
    print(green_arr)


def save_datas_with_labels(np_arrays):
    """
    存储已经由孤立森林学习过的带有标签的数据
    :param np_arrays:
    :return:
    """
    pass


def str_to_time_hour_minute(time):
    week = datetime.strptime(re.split(r" ", time)[0], "%Y/%m/%d").weekday()
    year, month, day, hour, minute, secend = re.split(r"[/ :]", time)
    print(week, hour, minute)
    return [hour, minute, week]


def translate_to_xgboost_datas(np_array):
    """
    将孤立森林处理过的数据转换成xgboost能够识别的数据，时间格式上转换
    :param np_arrays:
    :return:
    """
    hour_minute_week_array = [str_to_time_hour_minute(time) for time in np_array[1:, 1]]
    print(hour_minute_week_array)
    hour = []
    minute = []
    week = []
    for hour_minute_week in hour_minute_week_array:
        hour.append(int(hour_minute_week[0]))
        minute.append(int(hour_minute_week[1]))
        week.append((int(hour_minute_week[2])))
    hour.insert(0, "hour")
    minute.insert(0, "minute")
    week.insert(0, "week")
    # 删除时间一列
    np_array = np.delete(np_array, 1, axis = 1)
    # 增加分钟一列
    np_array = np.insert(np_array, 1, values = minute, axis = 1)
    # 增加小时一列
    np_array = np.insert(np_array, 1, values = hour, axis = 1)
    # 增加星期一列
    np_array = np.insert(np_array, 1, values = week, axis = 1)
    print(np_array)
    return np_array


cases = load_csv("../file/customs_test2.csv")
isolate1 = Isolate('2_7', cases)
np_array = isolate1.merge_arrays()
print(np_array[1:, 1])
translate_to_xgboost_datas(np_array)
