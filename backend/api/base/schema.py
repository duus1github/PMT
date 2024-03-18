#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:schema.py
@date:2023/10/9 16:56
@desc:''
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSch(BaseModel):
    searchValue: Optional[str] = None  # 搜索值
    createBy: Optional[str] = None  # 创建者
    createTime: Optional[datetime] = None  # 搜索值
    # updateBy: Optional[str] = None  # 更新者
    updateTime: Optional[datetime] = None  # 更新时间
    # remark: Optional[str] = None  # 备注
    # params: Optional[Dict] = None  # 请求参数