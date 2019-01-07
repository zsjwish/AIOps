#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 17:25
# @Author  : zsj
# @File    : mysql_operation.py
# @Description: 对数据库的操作，用于存储、查询、更改打标后的数据

import pymysql

from isolate_model.base_function import load_csv
from isolate_model.isolate_class import Isolate


def connectdb():
    """
    打开数据库连接
    :return:
    """
    db = pymysql.connect("localhost", "root", "123", "aiops")
    print('已连接数据库')
    return db


def query_table(db, table_name):
    """
    检查数据库中是否存在表table_name
    :param db: 已经连接的数据库
    :param table_name: 要查询的表的名字
    :return:如果表存在则返回True，否则返回False
    """
    cursor = db.cursor()
    sql = "select distinct t.table_name, n.SCHEMA_NAME " \
          "from " \
          "information_schema.TABLES t, information_schema.SCHEMATA n " \
          "where " \
          "t.table_name = '%s' and n.SCHEMA_NAME = 'aiops';" % (table_name)
    res = cursor.execute(sql)
    return res == 1


def create_table(db, np_array_field, table_name):
    """
    创建数据库表，
    :param db:
    :param np_array_field: 表字段名
    :param table_name: 表名
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    length = len(np_array_field)
    # 创建kpi和label的字段名,kpi都是float类型，label是int类型，且从第三列开始，前两列为host_id,timestamp
    kpi_sql = ""
    for i in range(2, length - 1):
        kpi_sql += "`%s` float," % (np_array_field[i])
    kpi_sql += "`label` int"

    # 创建表sql语句，加入一个id自增，因为一分钟内可能有多条数据
    sql = "create table `%s`(`id` int auto_increment primary key, `time` timestamp not null," % (
        table_name) + kpi_sql + ");"
    print(sql)

    # 创建表
    cursor.execute(sql)


def insert_datas(db, np_array):
    """
    训练时批量插入数据到表中
    :param db:
    :param np_array: 整个数据集，包括第一行字段名和后面的数据行
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    table_name = np_array[1, 0]

    # 插入的字段名，因为有一个主键是自增的
    fileds = "time,"
    for filed in np_array[0, 2:]:
        fileds += filed + ","
    fileds = fileds[:-1]

    # 待插入的数据，格式为(time,kpi_1...kpi_n, label),(time,kpi_1...kpi_n, label)...(time,kpi_1...kpi_n, label)
    datas_sql = ""
    for data in np_array[1:]:
        datas_sql += "('%s'," % (data[1])
        for i in range(2, len(data) - 1):
            datas_sql += "%f" % (float(data[i])) + ","
        datas_sql += "%d" % (int(data[-1])) + "),"
    datas_sql = datas_sql[:-1]

    # sql 插入语句,确定表名，字段名（有自增字段）,和插入内容
    sql = "INSERT INTO `%s`(%s) VALUES %s" % (table_name, fileds, datas_sql)
    print(sql)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果失败则回滚
        print('插入数据失败!')
        db.rollback()


def query_datas(db, table_name, label=(0, 1), start_time=0, end_time=0):
    """
    按条件查询数据库
    :param db:
    :param table_name:表名
    :param label: 标签
    :param start_time:
    :param end_time:
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    condition = ""
    if start_time != 0 and end_time != 0:
        condition = "and `time` between '%s' and '%s'" % (start_time, end_time)
    elif start_time != 0:
        condition = "and `time` >= '%s'" % start_time
    elif end_time != 0:
        condition = "and `time` <= '%s'" % end_time
    if label == 0 or label == 1:
        condition += "and label = %d" % label

    # SQL 查询语句
    # sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM `%s` where 1=1 %s" % (table_name, condition)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print("Error: unable to fecth data")
        return None


def update_datas(db, table_name, label, start_time=0, end_time=0):
    """
    更新数据库表数据label
    :param db:
    :param table_name: 表名
    :param start_time: 开始时间
    :param end_time: 截止时间
    :param label: 要更改成的label
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    condition = ""
    if start_time != 0 and end_time != 0:
        condition = "and `time` between '%s' and '%s'" % (start_time, end_time)
    elif start_time != 0:
        condition = "and `time` >= '%s'" % start_time
    elif end_time != 0:
        condition = "and `time` <= '%s'" % end_time

    # SQL 更新语句
    sql = "UPDATE `%s` SET label = %d where 1 = 1  %s" % (table_name, label, condition)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print('更新数据失败!')
        # 发生错误时回滚
        db.rollback()


def drop_table(db, table_name):
    """
    删除某表
    :param db:
    :param table_name:要删除的表名
    :return:
    """
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    sql = "drop table `%s`" % (table_name)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        print('删除数据库表失败!')
        # 发生错误时回滚
        db.rollback()


def delete_datas(db, table_name, start_time=0, end_time=0):
    """
    按时间区间删除数据
    :param db: 数据库
    :param table_name: 表名
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return:
    """
    cursor = db.cursor()
    condition = ""
    if start_time != 0 and end_time != 0:
        condition = "and `time` between '%s' and '%s'" % (start_time, end_time)
    elif start_time != 0:
        condition = "and `time` >= '%s'" % start_time
    elif end_time != 0:
        condition = "and `time` <= '%s'" % end_time

    sql = "delete from `%s` where 1=1  %s" % (table_name, condition)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print('删除数据失败!')
        # 发生错误时回滚
        db.rollback()


def closedb(db):
    """
    关闭数据库连接
    :param db:
    :return:
    """
    db.close()


def main():
    cases = load_csv("../file/customs_test2.csv")
    isolate1 = Isolate('2_7', cases)
    # isolate1.init_model()
    arr = isolate1.merge_arrays()
    db = connectdb()  # 连接MySQL数据库
    print(query_table(db, "student1"))
    print(query_table(db, "student"))
    table_name = arr[1, 0]
    # createtable(db, arr[0], table_name)  # 创建表
    insert_datas(db, arr)  # 插入数据
    query_datas(db, table_name)
    delete_datas(db, table_name)
    query_datas(db, table_name)
    # print('\n插入数据后:')
    # querydb(db)
    # deletedb(db)        # 删除数据
    # print('\n删除数据后:')
    # querydb(db)
    # updatedb(db)        # 更新数据
    # print('\n更新数据后:')
    # querydb(db)

    closedb(db)  # 关闭数据库


if __name__ == '__main__':
    main()
