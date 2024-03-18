#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:config.py
@date:2023/10/14 10:38
@desc:''
"""
import argparse

parser = argparse.ArgumentParser(description="Run dataprocess.")
parser.add_argument('--batch_size', nargs='?', default=64,
                    help='number of samples in one batch')
parser.add_argument('--epochs', nargs='?', default=10,  # 150
                    help='number of epochs in SGD')
parser.add_argument('--lr', nargs='?', default=1e-3,
                    help='learning rate for the SGD')
parser.add_argument('--device', nargs='?', default='cpu',
                    help='training device')
args = parser.parse_args()
