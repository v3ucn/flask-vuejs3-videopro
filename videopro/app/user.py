# 用户模块


import tornado.web


from app.base import BaseHandler

from model.models import db,UserModel,redis

from utils.util import make_password,check_none,Token,check_token,get_random_color,check_code,CheckRe,Robot,create_code,save_code,SimpleFactory,PhoneLogin,check_admin,Page,Rbac,role_dict,FileManager


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


import aiofiles



# 角色和前端入口菜单的对应关系

role_menu = {


        1:[{"name":"用户中心","url":"/user_center"},{"name":"视频上传","url":"/upload_video"}],

        2:[{"name":"用户中心","url":"/user_center"},{"name":"视频上传","url":"/upload_video"},{"name":"后台管理","url":"/admin"},{"name":"角色管理","url":"/role"}],
        3:[{"name":"审核视频","url":"/audit_video"}],


}



# 后台首页接口

class AdminListHandler(BaseHandler):


    # 获取对应字段

    def get_field(self,key):

        dicts = {"username":"a.username","create_time":"a.create_time","rid":"b.name"}

        return dicts[key]


    @check_token
    @check_admin
    async def get(self):


        # 接收参数

        keyword = self.get_argument("keyword",None)

        selected = self.get_argument("selected",None)

        orderby = self.get_argument("orderby","a.id desc")

        page = self.get_argument("page",1)


        # 筛选条件sql

        _where = ""

        if keyword:

            field = self.get_field(selected)

            _where += f" and {field} like '%%{keyword}%%' "


        # 实例化对象

        p = Page("user")

        # 返回数据

        userlist = await p.get_data(page,UserModel,"user",["a.id","a.username","a.create_time","b.name as rid"],orderby,"role",_where,["rid","id"])

        # 返回总个数

        total = await p.get_count(UserModel,_where)

        self.finish({"errcode":0,"data":userlist,"total":total,"pagesize":p.pagesize})





# 后台校验接口

class AdminHandler(BaseHandler):


    # 菜单入口
    @check_token
    async def post(self):


        if Rbac().check_role(self.rid,role_dict[2]):

            self.finish({"errcode":0,"menu":role_menu[2]})

        elif Rbac().check_role(self.rid,role_dict[1]):

            self.finish({"errcode":0,"menu":role_menu[1]})

        else:

            self.finish({"errcode":0,"menu":role_menu[3]})


    
    @check_token
    @check_admin
    async def get(self):


        self.finish({"errcode":0,"msg":"欢迎来到后台"})






# Gitee三方登录

class Gitee(BaseHandler):

    # 返回url
    async def post(self):

        self.finish({"errcode":0,"url":SimpleFactory.get_object("gitee").get_url()})


    # 回调接口
    async def get(self):

        code = self.get_argument("code",None)

        gitee = SimpleFactory.get_object("gitee")

        # 通过工厂调用获取用户信息
        name,avatar_url = gitee.get_info(code)

        # 判断用户账号
        user = await gitee.check_user(name,avatar_url)

        # 生成token
        token,refresh_token,user.avatar = await gitee.create_token(user)

        self.redirect(f"http://localhost:8080/jump?username={name}&token={token}&refresh_token={refresh_token}&avatar={avatar_url}")


# 钉钉三方登录

class Dingding(BaseHandler):

    # 返回url接口
    async def post(self):

        self.finish({"errcode":0,"url":SimpleFactory.get_object("dingding").get_url()})


    # 接收返回的code
    async def get(self):

        code = self.get_argument("code",None)

        # 抽象类实例 

        dingding = SimpleFactory.get_object("dingding")

        # 获取用户信息

        user = dingding.get_info(code)

        # 判断用户账号

        res = await dingding.check_user(user)

        # 生成token

        token,refresh_token = await dingding.create_token(res)

        # 需要进行重定向跳转

        self.redirect(f"http://localhost:8080/jump?username={user}&token={token}&refresh_token={refresh_token}")




# 图像文件流接口

class ImageCode(BaseHandler):

    async def get(self):


        # 接收参数

        username = self.get_argument("username",None)


        # 画布  宽  高

        img_size = (120,50)

        # 定义图对象

        image = Image.new("RGB",img_size,"white")

        # 定义画笔对象

        draw = ImageDraw.Draw(image,"RGB")


        # 定义字符串内容

        source = "0123456789"

        # 定义保存容器

        code_str = ""

        # 循环

        for i in range(4):

            # 随机获取下标

            tmp_num = random.randrange(len(source))

            # 通过下标取值

            random_str = source[tmp_num]

            # 收集随机生成的字符串

            code_str += random_str

            # 绘图

            draw.text((10+30*i,20),random_str,get_random_color())

        # 使用文件流来生成该图像

        # 生成内存缓冲区
        buf = io.BytesIO()
        # 指定图片类型
        image.save(buf,'png')


        # 保存验证码

        async with redis.client() as r:

            await r.set(username,code_str)

        # 指定响应头response头部信息

        self.set_header("Content-Type","image/png")

        return self.finish(buf.getvalue())









# 上传接口

class FileUploadHandler(BaseHandler):


    # 合并分片
    @check_token
    async def put(self):

        filename = self.get_argument("filename")


        # 开始合并

        fm = FileManager(self.uid)

        await fm.merge_slice(f"./static/{self.uid}",filename)

        self.finish({"errcode":0,"msg":"合并成功","filename":filename,"uid":self.uid})



    # 头像保存逻辑

    async def save_avatar(self,uid,filename):

        # 查询

        user = await db.get(UserModel.select().where(UserModel.id==uid))

        # 修改头像
        user.avatar = filename

        await db.update(user)


    # post进行上传
    @check_token
    async def post(self):


        # 设置上传类型

        upload_type = self.get_argument("upload_type","avatar")


        count = self.get_argument("count")


        # FileManager 创建目录

        fm = FileManager(self.uid)

        fm.create_dir("./static")


        # 接收文件

        file = self.request.files["file"]

        filename = ""

        # 写文件

        for meta in file:

            filename = meta["filename"]

            # with open(f"./static/{meta['filename']}","wb") as f:

            #     f.write(meta["body"])


            async with aiofiles.open(f"./static/{self.uid}/{meta['filename']}_{count}","wb") as f:

                # 异步写入
                await f.write(meta["body"])



        # 后续存储业务

        if upload_type == "avatar":

            await self.save_avatar(self.uid,filename)


        self.finish({"errcode":0,"msg":"文件上传成功","filename":filename,"uid":self.uid})


# 用户信息接口

class UserInfoHandler(BaseHandler):

    # 更新token操作
    async def put(self):

        # 接收refresh_token

        refresh_token = self.get_argument("refresh_token",None)

        # 读取redis内的refresh_token

        async with redis.client() as r:

            refresh_redis = await r.get(refresh_token)

        if not refresh_redis:

            return self.finish({"errcode":1,"msg":"您没有资格生成新token,请重新登录"})


        # 重新生成新的token

        tk = Token()

        token = tk.encode({"uid":refresh_redis})


        # 删除refresh_token

        async with redis.client() as r:

            await r.delete(refresh_token)


        # 重新生成refresh_token

        refresh_token = tk.encode({"uid":refresh_redis})


        # 写数据库

        async with redis.client() as r:

            await r.set(refresh_token,refresh_redis)


        self.finish({"errcode":0,"token":token,"refresh_token":refresh_token})




    # 用户信息接口
    @check_token
    async def get(self):


        # # 通过请求头来进行取值

        # token = self.request.headers.get("token",None)

        # # 解密

        # try:

        #     data = Token().decode(token)

        # except Exception as e:

        #     print(str(e))

        #     return self.finish({"errcode":1,"msg":"您的token不合法"})


        # 查询

        user = await db.get(UserModel.select().where(UserModel.id==self.uid))


        self.finish({"errcode":0,"filename":user.avatar})


# 手机验证码接口
class PhoneHandler(BaseHandler):


    async def post(self):

        phone = self.get_argument("phone",None)


        # 先生成四位随机码

        code = create_code()

        # Robot().send(code,phone)

        # 保存验证码

        await save_code(phone,code)


        self.finish({"errcode":0,"msg":"短信发送成功"})





class UserHandler(BaseHandler):


    async def login_check_code(self,key,code):


        # 判断验证码逻辑

        res = await check_code(key,code)

        if not res:

            return self.finish({"errcode":4,"msg":"您的验证码有误"})


    # 手机号登录方式

    async def phone_login(self,phone,code):


        # 校验手机号

        if not CheckRe().check_phone(phone):

            return self.finish({"errcode":1,"msg":"您的手机号格式有误"})


        # 校验短信

        res = await check_code(f"{phone}_msg",code)

        if not res:

            return self.finish({"errcode":2,"msg":"短信校验失败"})     


        # 是否时首次使用手机号进行登录

        # pl = PhoneLogin(phone)

        pl = SimpleFactory.get_object("phone",phone)

        user = await pl.check_user()

        token,refresh_token = await pl.create_token(user)

        self.finish({"errcode":0,"msg":"登录成功","username":user.username,"token":token,"refresh_token":refresh_token})


    # 账号密码登录方式

    async def user_password_login(self,username,password):

        # 查验当前用户是否在黑名单里

        async with redis.client() as r:

            res = await r.get(f"{username}_black")


        if res:

            return self.finish({"errcode":3,"msg":"您的账号已经被封禁"})


        # 获取错误次数的计数器

        async with redis.client() as r:

            num = await r.get(f"{username}_num")


        if num and int(num) >= 3:

            return self.finish({"errcode":4,"msg":"您已经错误次数"})




        # 查询

        try:

            user = await db.get(UserModel.select().where(   (UserModel.username==username)  &  (UserModel.password==make_password(password))     ))


            # 生成token

            token = Token().encode({"uid":user.id})

            # 生成refresh_token

            refresh_token = Token().encode({"uid":user.id})


            print(refresh_token)

            # 写数据库

            async with redis.client() as r:

                await r.set(refresh_token,user.id)




        except Exception as e:

            print(str(e))

            if num:

                async with redis.client() as r:

                    await r.incr(f"{username}_num")

            else:

                async with redis.client() as r:

                    await r.setex(f"{username}_num",30,1)




            return self.finish({"errcode":2,"msg":"您的账号或者密码有误"})


        self.finish({"errcode":0,"msg":"登录成功","username":user.username,"token":token,"refresh_token":refresh_token,"avatar":user.avatar})







    # 用户登录
    async def get(self):


        # 用户名
        username = self.get_argument("username",None)


        # 密码
        password = self.get_argument("password",None)


        # 手机号

        phone = self.get_argument("phone",None)


        # code 验证码

        code = self.get_argument("code",None)


        msg = self.get_argument("msg",None)


        # 登录模式

        login_type = self.get_argument("login_type",None)


        if login_type == "1":

            # 非空验证

            res = check_none([["username",username],["password",password],["code",code]])

            # 判断是否被拦截

            if res:

                return self.finish(res)


            await self.login_check_code(username,code)


            await self.user_password_login(username,password)

        else:


            # 非空验证

            res = check_none([["phone",phone],["code",code]])

            # 判断是否被拦截

            if res:

                return self.finish(res)

            await self.login_check_code(phone,code)

            await self.phone_login(phone,msg)


        







    # 用户注册

    async def post(self):

        # 接收参数

        # 用户名
        username = self.get_argument("username",None)

        print(username)

        if not username:

            return self.finish({"errcode":1,"msg":"用户名不能为空"})

        # 密码
        password = self.get_argument("password",None)

        # 手机号
        phone = self.get_argument("phone",None)


        # print(username)

        # print(password)

        # print(phone)


        # return self.finish({"errcode":2,"username":username,"password":password,"phone":phone})


        # 异步入库

        try:

            res = await db.create(UserModel,username=username,password=make_password(password),phone=phone)

        except Exception as e:

            print(str(e))

            return self.finish({"errcode":2,"msg":"用户名或者手机号重复"})


        self.finish({"errcode":0,"msg":"恭喜，注册成功"})


# 声明路由

urlpatterns = [

        (r"/user/",UserHandler),
        (r"/userinfo/",UserInfoHandler),
        (r"/upload/",FileUploadHandler),
        (r"/code/",ImageCode),
        (r"/phone/",PhoneHandler),
        (r"/dingding_back/",Dingding),
        (r"/gitee_back/",Gitee),
        (r"/admin/",AdminHandler),
        (r"/admin_index/",AdminListHandler),
        

]







