#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/10 21:04
@desc:''
"""
from pydantic import BaseModel


class ProjectForm(BaseModel):
    name: str


class ProjectResult(BaseModel):

    name: str
    user_id: str
    # folder_id: str

