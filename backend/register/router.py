#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/9 16:30
@desc:''
"""
from fastapi import FastAPI

from api import api_router


def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(api_router.router)  # 虚拟数据的api
    # 显示所有路由
    # routes = app.routes
    # for route in routes:
    #     print(route)