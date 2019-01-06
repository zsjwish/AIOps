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


def createtable(db, np_array_field, table_name):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    length = len(np_array_field)
    # 创建kpi和label的字段名,kpi都是float类型，label是int类型，且从第三列开始，前两列为host_id,timestamp
    kpi_sql = ""
    for i in range(2, length - 1):
        kpi_sql += "`%s` float," % (np_array_field[i])
    kpi_sql += "`label` int"

    sql = "create table `%s`(`id` int auto_increment primary key, `time` timestamp not null," % (table_name) + kpi_sql + ");"
    print(sql)

    # 创建表
    cursor.execute(sql)


def insertdb(db, np_array, table_name):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    fileds = "time,"
    for filed in np_array[0, 2:]:
        fileds += filed + ","
    fileds = fileds[:-1]
    print(fileds)
    datas_sql = ""
    for data in np_array[1:]:
        datas_sql += "('%s'," % (data[1])
        for i in range(2, len(data) - 1):
            datas_sql += "%f" % (float(data[i])) + ","
        datas_sql += "%d" % (int(data[-1])) + "),"
    datas_sql = datas_sql[:-1]
    print(datas_sql)
    # SQL 插入语句
    sql = """INSERT INTO `%s`(%s) VALUES %s""" % (table_name, fileds, datas_sql)
    print(sql)
    # sql = "INSERT INTO Student(ID, Name, Grade) \
    #    VALUES ('%s', '%s', '%d')" % \
    #    ('001', 'HP', 60)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        print('插入数据失败!')
        db.rollback()


def querydb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    # sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM Student"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            ID = row[0]
            Name = row[1]
            Grade = row[2]
            # 打印结果
            print("ID: %s, Name: %s, Grade: %d" % \
                  (ID, Name, Grade))
    except:
        print("Error: unable to fecth data")


def deletedb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    sql = "DELETE FROM Student WHERE Grade = '%d'" % (100)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        print('删除数据失败!')
        # 发生错误时回滚
        db.rollback()


def updatedb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql = "UPDATE Student SET Grade = Grade + 3 WHERE ID = '%s'" % ('003')

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print('更新数据失败!')
        # 发生错误时回滚
        db.rollback()


def closedb(db):
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
    insertdb(db, arr, table_name)  # 插入数据
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
