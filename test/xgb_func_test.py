#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/11 17:52
# @Author  : zsj
# @File    : xgb_func_test.py
# @Description:
from db.mysql_operation import insert_train_datas, connectdb, query_table, create_table
from isolate_model.base_function import load_csv
from isolate_model.isolate_class import Isolate
from xgboost_model.xgboost_class import Xgboost

cases = load_csv("../file/customs_cpu_test.csv")
isolate1 = Isolate('2_7', cases)
np_array = isolate1.merge_arrays()
table_name = np_array[1, 0]
db = connectdb()
# if not query_table(db, table_name):
#     create_table(db, np_array[0], table_name)
#
# insert_train_datas(db, np_array)


xgb1 = Xgboost(table_name)
