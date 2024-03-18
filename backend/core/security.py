#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:security.py
@date:2023/10/9 17:02
@desc:''
"""
# 密码加密算法
from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from api.base.crud import User_crud
from api.user.model import TokenData
from config.setting import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password, hashed_password) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_expires() -> datetime:
    """获取过期时间"""
    return datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = get_expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await User_crud.get_list_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# def create_access_token(data: dict, expires: Optional[datetime] = None) -> str:
#     """
#     生成token
#     :param expires: 过期时间
#     :param data: 存储数据
#     :param expires_delta: 有效时间
#     :return: 加密后的token
#     """
#     to_encode = data.copy()
#     if not expires:
#         expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expires})  # eg: {'sub': '1', scopes: ['items'] 'exp': '123'}
#     encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encode_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         print(token)
#         payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
#         # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         username: str = payload.get("sub")
#         if username is None:
#             raise Exception('用户名不存在')
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise Exception('用户认证失败')
#     user = await User_crud.get_db_or_none(phone_number=token_data.username)
#     if user is None:
#         raise Exception('用户不存在')
#     return user


def verify_token(user: str = Depends(get_current_user)):
    # if not token:
    #     raise HTTPException(
    #         status_code=HTTP_401_UNAUTHORIZED,
    #         detail='token 不正确'
    #     )
    # print('token')
    # user_id = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    print(user)
    return user
