#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/9 16:37
@desc:''
"""
import json

import kaptcha
from fastapi import APIRouter

from api.user.schema import LoginForm, RegisterForm
from api.user.service import LoginService, RegisterService
from core.result import ResultLogin, result_success

from utils.string_util import get_uuid

router = APIRouter(tags=["登录"])


def get_uuid_img():
    """获取uuid和img的base64"""
    code, image = kaptcha.Captcha().digit()
    img = image.split(",")[-1]
    uuid = get_uuid()
    return uuid, code, img


@router.post("/login", response_model=ResultLogin, summary='登录')
async def login(form: LoginForm):
    """
    登录
    先验证码，验证码失效或错误都会抛出异常。
    再验证用户名密码，成功则生成token，返回。
    """
    # 前面没有抛出异常，则验证密码并获取token
    token,user_id = await LoginService(form).validate_login_and_get_token()
    res ={'token':token,'userId':str(user_id)}
    return result_success(**{"token":token,"userId":str(user_id)})


@router.post("/register", response_model=ResultLogin, summary='注册')
async def register(form: RegisterForm):
    """
    注册接口
    """
    await RegisterService(form)

    return result_success(msg='操作成功')
