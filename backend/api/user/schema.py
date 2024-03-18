#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/9 16:42
@desc:''
"""
from typing import Optional

from fastapi import Form
from pydantic import BaseModel

from api.base.schema import BaseSch


class LoginForm(BaseModel):
    """LoginBody"""
    # code: Optional[str] = None
    username:Optional[str]=None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    # uuid: Optional[str] = None


class RegisterForm(BaseModel):
    """register body"""
    username: str
    phone_number: str
    password: str
from typing import Optional, List


class OAuth2PasswordRequestForm:
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.phone_number=username
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

class UserAdd(BaseSch):
    # deptId: Optional[int] = None  # 部门ID
    # email: Optional[str] = None  # 用户邮箱
    phone_num: Optional[str] = None  # 手机号码
    # sex: Optional[str] = None  # 用户性别,0=男,1=女,2=未知
    name: Optional[str] = None  # 用户账号
    # nickName: Optional[str] = None  # 用户昵称
    status: Optional[str] = None  # 帐号状态,0=正常,1=停用
    password: Optional[str] = None  # 密码
    # postIds: Optional[List[int]] = None  # 岗位组
    # roleIds: Optional[List[int]] = None  # 角色组


class UserSch(UserAdd):
    # userId: Optional[int] = None  # 用户ID
    # avatar: Optional[str] = None  # 用户头像
    delFlag: Optional[str] = None  # 删除标志（0代表存在 2代表删除）
    # loginIp: Optional[str] = None  # 最后登录IP
    # loginDate: Optional[datetime] = None  # 最后登录时间

    # dept: Optional[SysDeptSch] = None  # 部门对象
    # roles: Optional[List[SysRoleSch]] = None  # 角色对象
    # admin: Optional[bool] = None

    class Config:
        fields = {'password': {'exclude': True}}