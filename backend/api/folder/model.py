#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:model.py
@date:2023/10/13 16:41
@desc:''
"""
from api.base.model import AbstractModel, MixinTimeFiled
from tortoise import fields


class Folder(AbstractModel, MixinTimeFiled):
    name = fields.CharField(max_length=32, unique=True)
    project_id = fields.UUIDField()

    class Meta:
        table = 'folder'
        table_discription = '文件夹表'
