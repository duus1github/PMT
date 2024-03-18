#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:schema.py
@date:2023/10/9 20:16
@desc:''
"""
from tortoise import models, fields


class AbstractModel(models.Model):
    # 主键id
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class MixinTimeFiled:
    created_time = fields.DatetimeField(null=True, auto_now_add=True)
    modify_time = fields.DatetimeField(null=True, auto_now=True)
