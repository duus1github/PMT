#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:string_util.py
@date:2023/10/9 16:40
@desc:''
"""
import uuid


def get_uuid() -> str:
    """生成uuid"""
    return str(uuid.uuid4())
