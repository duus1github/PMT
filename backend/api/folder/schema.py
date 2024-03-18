#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:schema.py
@date:2023/10/13 16:41
@desc:''
"""
from uuid import UUID

from pydantic import BaseModel


class FolderForm(BaseModel):
    name: str
    project_id:UUID

