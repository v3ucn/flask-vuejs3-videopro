# 角色模块


import tornado.web


from app.base import BaseHandler

from model.models import db,UserModel,redis,RoleModel,VideoModel

from utils.util import make_password,check_none,Token,check_token,get_random_color,check_code,CheckRe,Robot,create_code,save_code,SimpleFactory,PhoneLogin,check_admin,Page,PageSlice,check_role


# 导入绘制图库
from PIL import ImageDraw,Image

import io

import random

import time

import json

import base64

import urllib.parse

import requests

import hmac

import hashlib

from playhouse.shortcuts import model_to_dict


# 审核接口

class AuditHandler(BaseHandler):


    # 审核列表页接口
    @check_token
    async def get(self):


        # 查询当前审核员的视频列表

        videolist = await db.execute(VideoModel.raw(f" select a.src,b.username as uid,b.id as id from video a left join user b on a.uid = b.id where a.audit_id = {self.uid}; "))

        # 序列化操作

        videolist = [model_to_dict(x) for x in videolist]


        self.finish({"errcode":0,"data":videolist})





# 基础操作类

class BaseManage(BaseHandler):


    # 获取单一数据

    async def get_one(self,model,id):


        data = await db.get(model,id=id)

        return data

    # 获取批量数据
    async def get_all(self,model):

        data = await db.execute(model.select())

        return data

    # 创建

    async def create(self,model,data):

        await db.create(model,**data)

        return True


    # 更新

    async def update(self,model,id,data):


        data_one = await db.get(model,id=id)

        model.update(**data).where(model.id==data.id).execute()

        return True


    # 物理删除
    async def delete(self,model,id):

        data_one = await db.get(model,id=id)

        await db.delete(data_one)


        return True



    # 序列化

    def my_model_to_dict(self,data,data_type=0):


        if data_type == 0:

            return model_to_dict(data)

        else:

            return [model_to_dict(x) for x in data]


# 角色接口

class RoleListHandler(BaseManage):


    async def put(self):

        rid = self.get_argument("id",None)

        name = self.get_argument("name",None)



        # 查询

        role = await self.get_one(RoleModel,rid)


        role.name = name


        await db.update(role)


        self.finish({"errcode":0,"msg":"修改成功"})




    async def delete(self):

        rid = self.get_argument("id",None)

        # 查询

        role = await db.get(RoleModel,id=rid)

        await db.delete(role)


        self.finish({"errcode":0,"msg":"删除成功"})





    @check_token
    @check_admin
    async def post(self):

        name = self.get_argument("name",None)


        role = await db.create(RoleModel,name=name)


        self.finish({"errcode":0,"msg":"添加成功"})
    

    @check_token
    @check_admin
    async def get(self):


        # 页数
        page = self.get_argument("page",1)

        # 实例化对象

        ps = PageSlice("role",RoleModel)


        # 获取数据和总数

        data,total = await ps.get_data(page,["a.name","a.id","group_concat(b.username) as create_time"],"a.id desc","user","",["id","rid"])

        print(data)

        self.finish({"errcode":0,"data":data,"total":total,"pagesize":ps.pagesize})


# 声明路由

urlpatterns = [

        (r"/admin_rolelist/",RoleListHandler),
        (r"/audit/",AuditHandler),

]