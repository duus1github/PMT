#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:api_router.py
@date:2023/10/9 16:31
@desc:''
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from api import user, project, folder, train
from api.base.crud import User_crud
from api.user import views
from api.project import views
from api.folder import views
from api.train import views

from api.user.model import Token
from api.user.schema import OAuth2PasswordRequestForm

from config.setting import settings
from core.result import Result
from core.security import create_access_token

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(user.views.router)
router.include_router(project.views.router)
router.include_router(folder.views.router)
router.include_router(train.views.router)
# router.include_router(monitor.router)
# router.include_router(common.router)


@router.get("/", response_model=Result, summary='访问首页，提示语')
async def get_index():
    return "欢迎使用。"


# @router.post('/token',response_model=None)
# async def token(form_data: OAuth2PasswordRequestForm=Depends()):
#
#     token = await LoginService(form_data).validate_login_and_get_token()
#
#     return {'access_token':token,'token_type':'bearer'}
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User_crud.get_list_db(**{'username': form_data.username, 'password_hash': form_data.password})
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[0].username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
