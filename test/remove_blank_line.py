#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/2 11:41
# @Author  : zsj
# @File    : remove_blank_line.py
# @Description: remove blank line
import sys

def read_file(file_from, file_to):
    with open(file_from, encoding='UTF-8') as file_read:
        lines = file_read.readlines()
    with open(file_to, 'w+', encoding = 'UTF-8') as file_write:
        for i in lines:
            if i is None or i == '\n':
                continue
            file_write.write(i)

read_file("2.txt", "2.txt")
# read_file(sys.argv[1], sys.argv[2])