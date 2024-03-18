#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/10 20:55
@desc:''
"""
import json
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from api.base.crud import Project_crud
from api.project.schema import ProjectForm
from core.result import Result, result_success
from core.security import verify_token

router = APIRouter(tags=['项目'])


@router.post('/project/create', response_model=Result, summary='创建项目')
async def add_project(project: ProjectForm, current_user: UUID = Depends(verify_token)):
    # todo:先判断该用户名下是否存在该项目名称，没有则添加，否则提示用户已存在
    project_dict = {'name': project.name, 'user_id': current_user[0].id}
    project_count = await Project_crud.get_list_count(**project_dict)
    if project_count == 0:
        await Project_crud.add_db(**project_dict)
    else:
        return result_success(msg='您创建的项目以存在！')
    return result_success(msg='项目新增成功')


@router.delete('/project/del', response_model=Result, summary='删除项目')
async def del_project(current_user=Depends(verify_token)):
    pass


@router.post('/project/update', response_model=Result, summary='修改项目')
async def update_project(current_user=Depends(verify_token)):
    pass


@router.get('/project', response_model=None, summary='项目列表')
async def project(current_user=Depends(verify_token)):
    project_dict = {'user_id': current_user[0].id}
    project_list = await Project_crud.get_list_db(**project_dict)
    res_list = []
    for _project in project_list:
        res_dict = {
            'name': _project.name,
            'user_id': str(_project.user_id),
            'folder_id': _project.folder_id
        }
        res_list.append(res_dict)
    return ORJSONResponse(res_list)
