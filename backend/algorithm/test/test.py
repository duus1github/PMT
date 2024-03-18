#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:test.py
@date:2023/10/14 10:37
@desc:''
"""
import json

import torch
from torch.utils.data import DataLoader

from algorithm.data_process.config import args
from algorithm.data_process.dataprocess import DataProcess
from algorithm.model.resnet import ResNet18
from algorithm.train.train import evalute


def test_main(data_path):
    test_db = DataProcess(data_path, 224, mode='test')
    test_loader = DataLoader(test_db, batch_size=args.batch_size)
    model = ResNet18(5).to(args.device)
    # todo:加载最好的模型,然后进行测试
    model.load_state_dict(torch.load('best.model'))
    print('loaded from ckpt!')

    test_acc = evalute(model, test_loader)
    yield json.dumps({'test acc':test_acc})