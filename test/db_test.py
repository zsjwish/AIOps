#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 17:45
# @Author  : zsj
# @File    : db_test.py
# @Description:

print("I'm %s. I'm %d year old" % ('Vamei', 99))
print("SELECT DISTINCT t.table_name, n.SCHEMA_NAME "
      "FROM "
      "information_schema.TABLES t, information_schema.SCHEMATA n "
      "WHERE "
      "t.table_name = %s AND n.SCHEMA_NAME = %s" % ("zsj", "yll"))
table_name = "student"
print("DSELECT DISTINCT t.table_name, n.SCHEMA_NAME FROM "
                   "information_schema.TABLES t, information_schema.SCHEMATA n "
                   "WHERE t.table_name = %s AND n.SCHEMA_NAME = 'aiops';" % (table_name))
