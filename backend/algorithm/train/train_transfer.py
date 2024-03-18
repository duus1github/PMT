#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:train_transfer.py
@time:2022/05/24
@desc:''

"""
import argparse
import time

# import visdom
import torch
import torch.nn as nn
from sklearn.metrics import auc, roc_curve, average_precision_score, precision_score, recall_score, f1_score
from torch import optim
from torch.utils.data import DataLoader

# from dataprocess import Pokemon
# from resnet import ResNet18
from torchvision.models import resnet18

# from utils import Flatten
from cirs.algorithm.data_process.dataprocess import DataProcess
from cirs.algorithm.utils import Flatten

parser = argparse.ArgumentParser(description="Run pokemon.")
parser.add_argument('--batch_size', nargs='?', default=64,
                    help='number of samples in one batch')
parser.add_argument('--epochs', nargs='?', default=10,  # 150
                    help='number of epochs in SGD')
parser.add_argument('--lr', nargs='?', default=1e-3,
                    help='learning rate for the SGD')
parser.add_argument('--device', nargs='?', default='cpu',
                    help='training device')
args = parser.parse_args()

# 设置种子点
torch.manual_seed(1234)
# todo:导入数据
train_db = DataProcess('pokemon', 224, mode='train')
val_db = DataProcess('pokemon', 224, mode='val')
test_db = DataProcess('pokemon', 224, mode='test')
# todo:适用dataloader,处理数据
train_loader = DataLoader(train_db, batch_size=args.batch_size, shuffle=True, num_workers=4)
val_loader = DataLoader(val_db, batch_size=args.batch_size)
test_loader = DataLoader(test_db, batch_size=args.batch_size)


def evalute(model, loader):
    """
    输入模型，数据集，来跑结果，然后得到它们精确度
    """
    # todo:一些性能指标图
    # viz = visdom.Visdom()
    # viz.line([0], [-1], win='auc', opts=dict(title='auc'))
    # viz.line([0], [-1], win='average_precision_score', opts=dict(title='average_precision_score'))
    # viz.line([0], [-1], win='precision_score', opts=dict(title='precision_score'))
    # viz.line([0], [-1], win='recall_score', opts=dict(title='recall_score'))
    # viz.line([0], [-1], win='f1_score', opts=dict(title='f1_score'))

    correct = 0
    total = len(loader.dataset)
    global_step = 0
    for x, y in loader:
        x, y = x.to(args.device), y.to(args.device)
        with torch.no_grad():
            logits = model(x)
            pred = logits.argmax(dim=1)
            # todo:！这里是画测试数据集的一些过程，好吧，我尝试了一下，这些基本都是二分类的性能评价。
            # print('pred:', pred, y)
            # time.sleep(2000)
            # false_positive_rate, true_positive_rate, thresholds = roc_curve(pred, y) # 这里报错了，因为roc是二类问题，而这里是多分类的问题啊
            # auc_ = auc(false_positive_rate, true_positive_rate)
            # ave = average_precision_score(pred, y)
            # pre_score = precision_score(pred, y)
            # re_score = recall_score(pred, y)
            # f1_score_ = f1_score(pred, y)

            # viz.line([auc_], [global_step], win='auc', update='append')
            # viz.line([ave], [global_step], win='average_precision_score', update='append')
            # viz.line([pre_score], [global_step], win='precision_score', update='append')
            # viz.line([re_score], [global_step], win='recall_score', update='append')
            # viz.line([f1_score_], [global_step], win='f1_score', update='append')

        correct += torch.eq(pred, y).sum().float().item()
        global_step += 1
    return correct / total


def main():
    # viz = visdom.Visdom()
    # model = ResNet18(5).to(args.device)
    trained_model = resnet18(pretrained=True)
    model = nn.Sequential(*list(trained_model.children())[:-1],
                          Flatten(),
                          nn.Linear(512, 5)
                          ).to(args.device)
    # x = torch.randn(2, 3, 224, 224)
    # print(model(x).shape)

    optimizer = optim.Adam(trained_model.parameters(), lr=args.lr)
    criteon = nn.CrossEntropyLoss()

    best_acc, best_epoch = 0, 0
    # todo:画图初始化
    # viz.line([0], [-1], win='loss', opts=dict(title='loss'))  # loss走势
    # viz.line([0], [-1], win='val_acc', opts=dict(title='val_acc'))  # 训练过程的测试集

    global_step = 0
    for epoch in range(args.epochs):
        for step, (x, y) in enumerate(train_loader):
            x, y = x.to(args.device), y.to(args.device)

            logits = model(x)
            loss = criteon(logits, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # todo：在这里加入性能参数的图像

            # viz.line([loss.item()], [global_step], win='loss', update='append')

            global_step += 1
        # todo:记录并保存最好的模型
        if epoch % 1 == 0:
            val_acc = evalute(model, val_loader)
            if val_acc > best_acc:
                best_epoch = epoch
                best_acc = val_acc
                torch.save(model.state_dict(), 'best.model')
                # viz.line([val_acc], [global_step], win='val_acc', update='append')
    print('best acc:', best_acc, 'best_epoch:', best_epoch)
    # todo:加载最好的模型
    model.load_state_dict(torch.load('best.model'))
    print('loaded from ckpt!')

    test_acc = evalute(model, test_loader)
    print('test acc.', test_acc)


if __name__ == '__main__':
    main()
