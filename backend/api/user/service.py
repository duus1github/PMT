#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/9 16:46
@desc:''
"""
from datetime import datetime

# from cirs.schemas.login import LoginForm
from typing import Optional

from fastapi import HTTPException

from api.base.crud import User_crud
from api.user.schema import LoginForm
from core.custom_exc import LoginException
from core.security import get_expires, create_access_token


class LoginService:
    """登录Service"""

    def __init__(self, form: Optional[LoginForm] = None, username: Optional[str] = None, pwd: Optional[str] = None):
        self.form: LoginForm = form
        if self.form is None:
            self.username = username
            self.password = pwd
        else:
            self.username = self.form.phone_number
            if self.username is None:
                self.username = self.form.username
            self.password = self.form.password

    async def validate_login_and_get_token(self):
        # 从数据库读取user
        user_db = await User_crud.get_db_or_none(phone_number=self.username)
        if user_db is None:
            raise LoginException("用户不存在")
        # if not verify_password(self.form.password, user_db.password_hash):
        if self.form.password != user_db.password_hash:
            raise LoginException("密码错误")
        if user_db.status == "1":
            raise LoginException("用户已停用")

        # 过期时间
        expires = get_expires()
        # 生成token
        token = create_access_token(data={"login_user_key": str(user_db.id), "sub": user_db.phone_number}, )

        return token, user_db.id


async def RegisterService(register_form):
    # todo:检查用户是否存在数据库中
    user_db = await User_crud.get_list_db()
    if register_form.phone_number in user_db:
        raise HTTPException(status_code=400, detail="手机号已存在")
    # todo:插入数据
    register_dict = {}
    register_dict['phone_number'] = int(register_form.phone_number)
    register_dict['username'] = register_form.username
    register_dict['password_hash'] = register_form.password
    await User_crud.add_db(**register_dict)
