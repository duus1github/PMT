#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:setting.py
@date:2023/10/9 15:50
@desc:'整个项目的配置文件'
"""
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    TITLE: str = 'fastAPI+vue'
    VERSION: str = 'v1.0'
    API_PREFIX: str = "/dev-api"
    DOCS_URL: str = "/dev-api/docs"
    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8080
    UVICORN_RELOAD: bool = True

    API_PREFIX: str = "/dev-api"  # 接口前缀
    GLOBAL_ENCODING: str = 'utf-8'  # 全局编码

    # Token
    # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = '1VkVF75nsNABBjK_7-qz7GtzNy3AMvktc9TCPwKczCk'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 3  # token过期时间: 60 m * 3 hour
    ALGORITHM: str = "HS512"  # 生成token的加密算法

    # Database
    DB_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)
    DB_HOST: str = ''
    DB_PORT: int = 3306
    DB_USER: str = ''
    DB_PASSWORD: str = ''
    DB_DATABASE: str = 'cirs'
    DB_CHARSET: str = 'utf8mb4'
    # DB_URL = f"sqlite://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
    DB_URL = "sqlite://cirs.sqlite3"
    DB_MODELS = ["api.user.model","api.project.model","api.folder.model"
        # "backend.cirs.models.file", "backend.cirs.models.folder", "backend.cirs.models.model",
                 # "backend.cirs.models.project1",
                 ]

# E:\WorkSpace\hobby\softwork\backend\cirs\models\model.py
settings = Settings()
