#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/13 21:32
@desc:''
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from algorithm.test.test import test_main
from algorithm.train.train import train_main
from api.base.crud import Project_crud

router = APIRouter()


@router.post('/train', response_model=None, summary='模型训练')
async def model_train(project_id: UUID, model: str):
    """
    1、模型训练部分，用户在前端指定数据集，和对应的模型，然后点击开始训练
    2、模型在训练的过程中，需要实时返回训练的数据，比如loss,val验证模型的值等，
    3、模型在训练结束之后，会保存这个模型到用户模型中，然后可以使用该模型进行测试。
    """
    # todo:输入图片数据，模型名称
    project_db = await Project_crud.get_db_or_none(id=project_id)
    # todo:调用模型开始训练
    return StreamingResponse(train_main(f'storage/{project_db.name}'))



@router.post('/test', response_model=None, summary='模型测试')
async def model_test(project_id: UUID, model: str):
    """
    1、用户指定训练好的模型，和对应的数据，进行模型测试
    2、输出对应的评价指标结果，包括f1socre,ROC,AUC等曲线。
    """
    project_db = await Project_crud.get_db_or_none(id=project_id)
    return StreamingResponse(test_main(f'storage/{project_db.name}'))
