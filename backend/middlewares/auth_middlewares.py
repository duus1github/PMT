#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:auth_middlewares.py.py
@date:2023/10/8 19:45
@desc:''
"""
from fastapi.middleware.cors import CORSMiddleware

from main import app

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

