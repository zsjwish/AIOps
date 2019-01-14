#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 17:45
# @Author  : zsj
# @File    : db_test.py
# @Description:
from db.mysql_operation import connectdb, create_table, query_table, query_datas, update_datas, delete_datas, \
    drop_table, insert_train_datas, closedb
from isolate_model.base_function import load_csv
from isolate_model.isolate_class import Isolate

cases = load_csv("../file/customs_msmq_test.csv")
isolate1 = Isolate('2_7', cases)
np_array = isolate1.merge_arrays()

db = connectdb()
table_name = np_array[1, 0]
# 判断是否存在该表
is_exists = query_table(db, table_name)
# 如果不存在则创建该表
if not is_exists:
    create_table(db, np_array[0], table_name)
# 插入数据
insert_train_datas(db, table_name, np_array[1:])
result = query_datas(db, table_name)
print(len(result))
