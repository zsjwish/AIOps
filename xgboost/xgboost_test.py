#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 16:38
# @Author  : zsj
# @File    : xgboost_test.py
# @Description:

import numpy as np
import scipy.sparse
import pickle
import xgboost as xgb

from isolate_model.base_function import load_csv, translate_to_xgboost_datas
from isolate_model.isolate_class import Isolate

cases = load_csv("../file/customs_test2.csv")
isolate1 = Isolate('2_7', cases)
np_array = isolate1.merge_arrays()
np_array = translate_to_xgboost_datas(np_array)

# 从文本文件加载文件，也是由xgboost生成的二进制缓冲区，加载能训练的文件，
print(np_array[1:, 1:-1].astype(float))
print(np_array[1:, -1].astype(int))
dtrain = xgb.DMatrix(np_array[1:, 1:-1].astype(float), label = np_array[1:, -1].astype(int))
dtest = xgb.DMatrix('../file/customs_test2.csv')

# 通过map指定参数，max_depth：树的最大深度，太大容易过拟合
# eta 步长 verbosity：1警告信息 objective：binary：logistic 二分类逻辑回归，输出概率
param = {'max_depth': 2, 'eta': 1, 'verbosity': 1, 'objective': 'binary:logistic'}

# specify validations set to watch performance
watchlist = [(dtrain, 'train')]
# num_round 提升的轮次数
num_round = 2
# 训练数据
bst = xgb.train(param, dtrain, num_round, watchlist)

# this is prediction
preds = bst.predict(dtest)
labels = dtest.get_label()
print('error=%f' % (sum(1 for i in range(len(preds)) if int(preds[i] > 0.5) != labels[i]) / float(len(preds))))
bst.save_model('0001.model')
# dump model
bst.dump_model('dump.raw.txt')
# dump model with feature map
bst.dump_model('dump.nice.txt', '../data/featmap.txt')

# save dmatrix into binary buffer
dtest.save_binary('dtest.buffer')
# save model
bst.save_model('xgb.model')
# load model and data in
bst2 = xgb.Booster(model_file = 'xgb.model')
dtest2 = xgb.DMatrix('dtest.buffer')
preds2 = bst2.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds2 - preds)) == 0

# alternatively, you can pickle the booster
pks = pickle.dumps(bst2)
# load model and data in
bst3 = pickle.loads(pks)
preds3 = bst3.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds3 - preds)) == 0

###
# build dmatrix from scipy.sparse
print('start running example of build DMatrix from scipy.sparse CSR Matrix')
labels = []
row = []
col = []
dat = []
i = 0
for l in open('../data/agaricus.txt.train'):
    np_array = l.split()
    labels.append(int(np_array[0]))
    for it in np_array[1:]:
        k, v = it.split(':')
        row.append(i);
        col.append(int(k));
        dat.append(float(v))
    i += 1
csr = scipy.sparse.csr_matrix((dat, (row, col)))
dtrain = xgb.DMatrix(csr, label = labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print('start running example of build DMatrix from scipy.sparse CSC Matrix')
# we can also construct from csc matrix
csc = scipy.sparse.csc_matrix((dat, (row, col)))
dtrain = xgb.DMatrix(csc, label = labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print('start running example of build DMatrix from numpy array')
# NOTE: npymat is numpy array, we will convert it into scipy.sparse.csr_matrix in internal implementation
# then convert to DMatrix
npymat = csr.todense()
dtrain = xgb.DMatrix(npymat, label = labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)
