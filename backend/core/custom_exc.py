#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:custom_exc.py
@date:2023/10/9 17:01
@desc:''
"""
class LoginException(Exception):
    """ 登录错误，包含验证码失效、验证码错误、用户名密码错误"""

    def __init__(self, err_desc: str = "用户名、密码、验证码错误或token失效"):
        self.err_desc = err_desc