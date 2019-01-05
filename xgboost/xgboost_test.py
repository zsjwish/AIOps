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

from isolate_model.base_function import load_csv
from isolate_model.isolate_class import Isolate

cases = load_csv("../file/customs_test2.csv")
isolate1 = Isolate('2_7', cases)
# isolate1.init_model()
arr = isolate1.merge_arrays()

# 从文本文件加载文件，也是由xgboost生成的二进制缓冲区，加载能训练的文件，
print(arr[1:, 0:-1])
print(arr[1:, -1])
dtrain = xgb.DMatrix(arr[1:, 0:-1], label = arr[1:, -1])
dtest = xgb.DMatrix('../data/agaricus.txt.test')

# 通过map指定参数，
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}

# specify validations set to watch performance
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 2
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
    arr = l.split()
    labels.append(int(arr[0]))
    for it in arr[1:]:
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
