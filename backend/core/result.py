#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:result.py
@date:2023/10/9 16:35
@desc:''
"""
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

SchemasType = TypeVar("SchemasType", bound=BaseModel)


class ResultLogin(BaseModel):
    """
    登陆结果
    成功返回：{"msg":"操作成功","code":200,"token":""}\n
    失败返回：{"msg":"验证码错误","code":500}或{"msg":"用户不存在/密码错误","code":500}\n
    """
    code: int
    msg: str
    token: Optional[str]
    userId:str


class Result(GenericModel, Generic[SchemasType]):
    """ 普通结果 """
    code: int
    msg: str


def result_success(code: int = 200, msg: str = "操作成功", **kwargs) -> dict:
    """返回结果"""
    kwargs.update({'code': code, 'msg': msg})
    # logger.debug(kwargs)
    return kwargs
