#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:train.py
@time:2022/05/24
@desc:''

"""
import json

import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from algorithm.data_process.config import args
from algorithm.data_process.dataprocess import DataProcess
from algorithm.model.resnet import ResNet18

# 设置种子点
torch.manual_seed(1234)


def evalute(model, loader):
    """
    计算预测正确数据和错误数据比例
    :param model:
    :param loader:
    :return:
    """
    correct = 0
    total = len(loader.dataset)
    for x, y in loader:
        x, y = x.to(args.device), y.to(args.device)
        with torch.no_grad():
            logits = model(x)
            pred = logits.argmax(dim=1)
        correct += torch.eq(pred, y).sum().float().item()
    return correct / total


def train_main(train_data_path):
    # todo:导入数据
    # train_db = DataProcess('pokemon', 224, mode='train')
    train_db = DataProcess(train_data_path, 224, mode='train')
    # val_db = DataProcess(, 224, mode='val')
    val_db = DataProcess(train_data_path, 224, mode='val')

    # todo:适用dataloader,处理数据
    train_loader = DataLoader(train_db, batch_size=args.batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_db, batch_size=args.batch_size)
    # viz = visdom.Visdom()
    model = ResNet18(5).to(args.device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    criteon = nn.CrossEntropyLoss()

    best_acc, best_epoch = 0, 0
    # viz.line([0], [-1], win='loss', opts=dict(title='loss'))
    # viz.line([0], [-1], win='val_acc', opts=dict(title='val_loss'))
    global_step = 0
    for epoch in tqdm(range(args.epochs)):
        for step, (x, y) in enumerate(train_loader):
            x, y = x.to(args.device), y.to(args.device)

            logits = model(x)
            loss = criteon(logits, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # viz.line([loss.item()], [global_step], win='loss', update='append')
            print(loss.item(), global_step)
            yield json.dumps({'loss':loss.item(), 'step':global_step})

            global_step += 1
        # todo:记录并保存最好的模型
        if epoch % 1 == 0:
            val_acc = evalute(model, val_loader)
            if val_acc > best_acc:
                best_epoch = epoch
                best_acc = val_acc
                torch.save(model.state_dict(), 'best.model')
                # viz.line([val_acc], [global_step], win='val_acc', update='append')
                print('val_acc:',val_acc,'global_step:',global_step)
                yield json.dumps({'val_acc':val_acc, 'step':global_step})
    print('best acc:', best_acc, 'best_epoch:', best_epoch)
    yield json.dumps({'best_acc':best_acc, 'best_epoch':best_epoch})

if __name__ == '__main__':
    main('storage/pokemon')
