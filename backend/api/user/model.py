#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:model.py
@date:2023/10/8 19:46
@desc:''
"""
from typing import Union

from pydantic import BaseModel
from tortoise import fields

from api.base.model import AbstractModel, MixinTimeFiled


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Users(AbstractModel, MixinTimeFiled):
    """
    The User model
    """
    username = fields.CharField(max_length=20, unique=True)
    phone_number = fields.IntField(max_length=11, unique=True)
    status = fields.IntField(default=1)  # 1为正常使用，0为删除
    password_hash = fields.CharField(max_length=128, null=True)

    class Meta:
        table = 'user'
        table_description = '用户信息表'
