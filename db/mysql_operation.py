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
    # 打开数据库连接
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

def createtable(db, np_array, table_name):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    length = len(np_array)
    kpi_sql = ""
    for i in range(2, length-1):
        kpi_sql += "`%s` float," % (np_array[i])
    kpi_sql += "`%s` int" % np_array[-1]

    sql = "create table `%s`(host_id char(255) not null primary key, `time` timestamp," % (table_name) + kpi_sql + ");"
    print(sql)

    # 创建Sutdent表
    cursor.execute(sql)

def insertdb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = """INSERT INTO Student
         VALUES ('001', 'CZQ', 70),
                ('002', 'LHQ', 80),
                ('003', 'MQ', 90),
                ('004', 'WH', 80),
                ('005', 'HP', 70),
                ('006', 'YF', 66),
                ('007', 'TEST', 100)"""

    #sql = "INSERT INTO Student(ID, Name, Grade) \
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
    #sql = "SELECT * FROM Student \
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
    cases = load_csv("../file/customs_test3.csv")

    # ##初始化模型
    isolate1 = Isolate('2_7', cases)
    # isolate1.init_model()
    arr = isolate1.merge_arrays()
    db = connectdb()    # 连接MySQL数据库
    print(query_table(db, "student1"))
    print(query_table(db, "student"))
    createtable(db, arr[0], arr[1, 0])     # 创建表
    # insertdb(db)        # 插入数据
    # print('\n插入数据后:')
    # querydb(db)
    # deletedb(db)        # 删除数据
    # print('\n删除数据后:')
    # querydb(db)
    # updatedb(db)        # 更新数据
    # print('\n更新数据后:')
    # querydb(db)

    closedb(db)         # 关闭数据库

if __name__ == '__main__':
    main()
