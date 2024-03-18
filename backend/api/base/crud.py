#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:schema.py
@date:2023/10/9 16:53
@desc:''
"""
from typing import TypeVar, Generic, Type, Optional, List

from pydantic import BaseModel
from tortoise import Model
from tortoise.queryset import QuerySet

from api.folder.model import Folder
from api.folder.schema import FolderForm
from api.project.model import Project
from api.project.schema import ProjectForm
from api.user.model import Users
from api.user.schema import UserAdd

ModelType = TypeVar("ModelType", bound=Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType], schema_model: Type[SchemaType]):
        """
        具有增删改查的默认方法的 CRUD 对象。
        """
        self.model = model
        self.schema_model = schema_model

    async def add_db(self, **kwargs) -> ModelType:
        """增加"""
        return await self.model.create(**kwargs)

    async def delete_db(self, **kwargs) -> int:
        """删除"""
        return await self.model.filter(**kwargs).delete()

    async def update_db(self, obj_db: ModelType, **kwargs):
        """修改"""
        await obj_db.update_from_dict(kwargs).save()

    def get_list_queryset(self, **kwargs) -> QuerySet[ModelType]:
        return self.model.filter(**kwargs)

    async def get_list_db(self, **kwargs) -> Optional[List[ModelType]]:
        """查询全部,自动将QuerySet转成list,createTime__range=(start, end)
        :param kwargs: 需要将None数据去除
        """
        return await self.model.filter(**kwargs).all()

    async def get_list_count(self, **kwargs) -> int:
        return len(await self.get_list_sch(**kwargs))

    async def get_list_db_page(self, pageNum=1, pageSize=10, **kwargs) -> Optional[List[ModelType]]:
        """查询全部,自动将QuerySet转成list,createTime__range=(start, end)
        :param kwargs: 需要将None数据去除
        """
        offset = (pageNum - 1) * pageSize
        return await self.model.filter(**kwargs).limit(pageSize).offset(offset).all()

    async def get_db_or_none(self, **kwargs) -> Optional[ModelType]:
        """查询"""
        return await self.model.get_or_none(**kwargs)

    async def add_sch(self, **kwargs) -> SchemaType:
        obj_db = await self.add_db(**kwargs)
        return self.schema_model.from_orm(obj_db)

    async def update_sch(self, obj: ModelType, **kwargs):
        await self.update_db(obj, **kwargs)

    async def get_sch_or_none(self, **kwargs) -> Optional[ModelType]:
        obj_db = await self.get_db_or_none(**kwargs)
        if obj_db:
            return self.schema_model.from_orm(obj_db)
        else:
            return None

    async def get_list_sch(self, **kwargs) -> List[SchemaType]:
        objs_db = await self.get_list_db(**kwargs)
        sch_list = []
        for obj in objs_db:
            sch_list.append(self.schema_model.from_orm(obj))
        return sch_list

    async def get_list_sch_page(self, pageNum=1, pageSize=10, **kwargs) -> List[SchemaType]:
        objs_db = await self.get_list_db_page(pageNum=pageNum, pageSize=pageSize, **kwargs)
        sch_list = []
        for obj in objs_db:
            sch_list.append(self.schema_model.from_orm(obj))
        return sch_list


User_crud = CRUDBase(Users, UserAdd)
Project_crud = CRUDBase(Project, ProjectForm)
Folder_crud = CRUDBase(Folder,FolderForm)
