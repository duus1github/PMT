#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/1/9 16:48
# @Author : zxiaosi
# @desc : 跨域请求
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_cors(app: FastAPI):
    """
    跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/
    https://www.cnblogs.com/poloyy/p/15347578.html
    """
    origins = [
        # "http://localhost.tiangolo.com",
        # "https://localhost.tiangolo.com",
        "http://localhost",
        "https://127.0.0.1:8080",
        "http://127.0.0.1:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # 允许访问的源
        allow_credentials=True,  # 支持 cookie
        # allow_methods=("GET", "POST", "PUT", "DELETE"),  # 允许使用的请求方法
        allow_methods=["*"],  # 允许使用的请求方法
        # allow_headers=("*", "authentication"),  # 允许携带的 Headers
        allow_headers=["*"],  # 允许携带的 Headers
    )
