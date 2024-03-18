#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:views.py
@date:2023/10/13 16:42
@desc:''
"""
import os.path
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, File, UploadFile, HTTPException

from api.base.crud import Folder_crud, Project_crud
from api.folder.schema import FolderForm
from core.result import result_success, Result

router = APIRouter(tags=['文件'])


@router.post("/folder/create", response_model=Result, summary='创建文件夹')
async def create(folder: FolderForm):  # 创建文件夹部分我觉得暂时可以不需要，就文件上传的时候，自动创建一个文件夹就行
    # todo:folder name不能重复
    folder_dict = {'name': folder.name, 'project_id': folder.project_id}
    folder_count = await Folder_crud.get_db_or_none(**folder_dict)
    if folder_count:
        raise HTTPException(status_code=400,detail='文件夹已存在')
    folder_db = await Folder_crud.add_db(**folder_dict)
    folder_name = folder_db.name
    return result_success(msg=f'{folder_name}创建成功')


@router.post('/upload_files', response_model=None, summary='上传文件')
async def upload_files(folder_id: Optional[UUID] = None, files: List[UploadFile] = File(...)):
    # todo:想创建一个文件夹，
    if folder_id is None:
        raise Exception('请先创建文件夹，在上传文件！')
    folder_db = await Folder_crud.get_db_or_none(id=folder_id)
    project_db = await Project_crud.get_db_or_none(id =folder_db.project_id)
    for file in files:
        save_folder=f'storage/{project_db.name}/{folder_db.name}'
        # if os.path.exists(f'cirs/storage/{project_name}'):
        #     os.mkdir(f'cirs/storage/{project_name}')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        with open(f"{save_folder}/{file.filename}", 'wb+') as f:
            for i in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
                f.write(i)
        f.close()
    return {"file_name": [file.filename for file in files]}
