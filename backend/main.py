#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:main.py
@date:2023/10/8 19:44
@desc:'fastpai项目的启动文件'
"""
import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config.setting import settings
from register.cors import register_cors
from register.router import register_router
from register.tortoise import register_orm

app = FastAPI(version=settings.VERSION, debug=settings.DEBUG,
              title=settings.TITLE, docs_url=settings.DOCS_URL,
              )


async def create_app():
    # 注册路由
    register_router(app)
    register_cors(app)
    # 注册数据库
    await register_orm(app)

@app.on_event("startup")
async def startup():
    # logger.info("startup")  # 初始化日志
    await create_app()  # 加载注册中心


if __name__ == '__main__':
    uvicorn.run(app='main:app', host=settings.UVICORN_HOST, port=settings.UVICORN_PORT, reload=settings.UVICORN_RELOAD)
