#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/9 15:37
@desc:''
"""
from tortoise import fields

from api.base.model import AbstractModel, MixinTimeFiled


class Project(AbstractModel, MixinTimeFiled):
    name = fields.CharField(max_length=64, unique=True)
    user_id = fields.UUIDField()


    class Meta:
        table = 'project'
        table_description = '项目表'
