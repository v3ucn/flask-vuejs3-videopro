import hashlib

import jwt

import datetime


# 设置模块的路径

import os,sys

# # 设置基础路径

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载项目路径

sys.path.append(base_path)

# 加载指定模块

sys.path.append(os.path.join(base_path,'model'))

sys.path.append(os.path.join(base_path,'config'))

from model.models import redis,db,UserModel,RoleModel

from config.settings import baidu_apikey,baidu_secret


import asyncio

import random

import re

import time

import hmac

import hashlib

import base64

import urllib.parse

import requests

import json


from abc import ABCMeta,abstractmethod

from playhouse.shortcuts import model_to_dict


import aiofiles


# 用户私聊记录类

class TalkLog:

    def __init__(self,uid,to_uid):

        sort_list = []

        sort_list.append(str(uid))
        sort_list.append(str(to_uid))

        sort_list.sort()

        self.key = "_".join(sort_list)


    # 返回聊天信息

    async def get(self):


        async with redis.client() as r:

            msglist = await r.lrange(self.key,0,-1)

        return [eval(x) for x in msglist]




    # 添加聊天信息

    async def add(self,username,msg,uid,msg_type):


        msg_dict = {"username":username,"msg":msg,"uid":uid,"msg_type":int(msg_type)}

        msg_dict = json.dumps(msg_dict,ensure_ascii=False)

        # 写入数据库

        async with redis.client() as r:

            await r.rpush(self.key,msg_dict)






if __name__ == '__main__':

    tl = TalkLog(17,10)

    print(asyncio.run(tl.get()))




# 用户关注类

class FollowFans:

    def __init__(self,uid):

        self.uid = uid


    # 添加关注或者粉丝

    async def zadd(self,uid,ztype="follow"):

        async with redis.client() as r:

            await r.zadd(f"{self.uid}:{ztype}",{uid:0})

    # 取消关注或者删除粉丝
    async def zrem(self,uid,ztype="follow"):

        async with redis.client() as r:

            await r.zrem(f"{self.uid}:{ztype}",uid)

    # 关注者列表或者粉丝列表
    async def zrange(self,ztype="follow"):

        async with redis.client() as r:

            userlist = await r.zrange(f"{self.uid}:{ztype}",0,-1)


        return userlist











# 实现审核队列系统

class AuditQueue:

    def __init__(self):

        self.key = "job"
        self.redis = redis

    # 入队 加权 优先级 vip

    async def push_vip(self,x:tuple) -> None:

        async with redis.client() as r:

            await r.lpush(self.key,x)

    # 出队  ack 幂等性确认

    async def pop_ack(self):

        async with redis.client() as r:

            item = await r.brpoplpush(self.key,"confirm_job")


        return item


    # 出队 加权
    async def pop_vip(self) -> tuple:

        # 高阶方法sorted

        # 获取审核队列

        async with redis.client() as r:

            job_list = await r.lrange(self.key,0,-1)

        job_list = [eval(x) for x in job_list]

        job_list = sorted(job_list,key=lambda x:x[1])

        # 出队

        return job_list.pop()



    # 入队方法

    async def push(self,vid:int):

        # self.q.append(vid)

        # self.q.insert(0,vid)

        # 操作redis进行入队操作
        async with redis.client() as r:

            await r.lpush(self.key,vid)

    # 出队方法
    async def pop(self) -> int:

        async with redis.client() as r:

            vid = await r.rpop(self.key)


        return vid

        

    # 查看队列是否为空
    def empty(self) -> bool:

        return not bool(self.q)





# 栈的实现

class Stack:

    def __init__(self):

        self.s = []

    # 入栈
    def push(self,item):

        self.s.append(item)

    # 出栈
    def pop(self):

        return self.s.pop()


# 利用栈解决十进制转二进制
def mybin(num):

    stack = Stack()

    while num != 0 :

        res = num % 2

        num = int(num/2)

        stack.push(res)

    return stack.s







# 文件管理模块

class FileManager:

    def __init__(self,uid):

        self.uid = uid


    # 合并分片文件

    async def merge_slice(self,src,filename):

        num = 0


        async with aiofiles.open(f"{src}/{filename}","ab") as target_file:

            while True:

                try:

                    # 读取分片文件
                    source_file = open(f"{src}/blob_{num}","rb")

                    # 写入

                    await target_file.write(source_file.read())

                    source_file.close()

                except Exception as e:

                    print(str(e))

                    break


                num = num + 1



    # 创建当前用户的目录

    def create_dir(self,src):


        if not os.path.exists(f"{src}/{self.uid}"):


            os.mkdir(f"{src}/{self.uid}")


    # 列出文件列表

    def filelist(self,src):

        return os.listdir(f"{src}/{self.uid}")


    # 删除文件

    def delfile(self,src,filename):


        os.remove(f"{src}/{self.uid}/{filename}")









# 异步操作文件


async def write_file():


    async with aiofiles.open("text.txt","w",encoding="utf-8") as f:

        # 异步写入
        await f.write("test")






# 位运算

# 角色容器  0b001  0b010  0b100

role_dict = {1:1,2:2,3:4}


# 角色控制类

class Rbac:


    # 检测当前用户是否有角色权限
    def check_role(self,user,role):


        # 位于运算进行检测

        if user & role:

            return True

        else:

            return False


    # 给用户的角色授权

    def update_role(self,user,role):

        # 位或运算

        return user | role

    # 取消用户角色

    def del_role(self,user,role):


        return user ^ role







# 切片分页类

class PageSlice:

    def __init__(self,table,model,pagesize=10):

        self.table = table

        self.model = model

        self.pagesize = pagesize

    # 获取数据

    async def get_data(self,page:int,fields:list,orderby:str,join_table:str,field:str,fkey:list):


        # 拼接搜索字段

        fields = ",".join(fields)

        # 分页

        start = (int(page) - 1) * self.pagesize

        end = start + self.pagesize
        
        sql = f" select {fields} from {self.table} a left join {join_table} b  on a.{fkey[0]} = b.{fkey[1]}  where a.id != 0  {field}  group by a.id  "

    
        #print(sql)

        # 进行异步查询

        userlist = await db.execute(self.model.raw(sql))

        # 序列化

        userlist = [model_to_dict(x) for x in userlist]



        # 排序两套方案  内置sort()  高阶方法sorted()

        # sort改变元对象顺序，sorted不会改变，而是返回一个新对象

        if orderby.find("desc") != -1:

            userlist.sort(key = lambda x:x["id"],reverse=True)


        # 返回数据总数

        total = len(userlist)

        userlist = userlist[start:end]

        #print(userlist)


        return userlist,total






# 通用分页类

class Page:

    def __init__(self,table,pagesize=3):


        self.table = table

        self.pagesize = pagesize

    # 返回当前页的数据

    async def get_data(self,page:int,model,table:str,fields:list,orderby:str,join_table:str,field:str,fkey:list):

        # 拼接搜索字段

        fields = ",".join(fields)

        # 分页

        start = (int(page) - 1) * self.pagesize

        num = self.pagesize
        
        sql = f" select {fields} from {table} a left join {join_table} b  on a.{fkey[0]} = b.{fkey[1]}  where a.id != 0  {field}  order by  {orderby} limit {start},{num}  "

        
        #print(sql)

        # 进行异步查询

        userlist = await db.execute(model.raw(sql))


        # 序列化

        userlist = [model_to_dict(x) for x in userlist]


        return userlist



    # 获取当前数据表的总页数

    async def get_all_page(self,model,field):

        # 先获取总个数
        total = await self.get_count(model,field)


        # 总个数  

        if total % self.pagesize == 0:

            return total // self.pagesize

        else: 

            return total // self.pagesize + 1


    # 获取总个数
    async def get_count(self,model,field=""):


        sql = f" select count(1) as id from  `{self.table}`  where id != 0  {field}  "

        table_count = await db.execute(model.raw(sql))

        table_count = [model_to_dict(x) for x in table_count]

        return table_count[0]["id"]



        # table_count = await db.execute(eval(f"{model}.raw('{sql}')"))










# 百度AI类

class BaiduAi:

    def __init__(self):

        self.apikey = baidu_apikey

        self.secret = baidu_secret

        # 初始化请求头

        self.headers = {"Content-Type":"application/x-www-form-urlencoded"}

        # 初始化识别接口地址

        self.url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    # 获取接口token

    def get_token(self):

        res = requests.get(f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.apikey}&client_secret={self.secret}")

        return res.json()["access_token"]


    # 自动化比对识别结果

    async def check_code(self,key,code):


        # 读取redis数据

        async with redis.client() as r:

            redis_code = r.get(key)


        if redis_code:

            if int(redis_code) == int(code):

                return True

            else:

                return False

        else:

            return False


    # 识别

    def check_img(self,token,img_src):

        # 根据图片地址读取图片内容

        with open(img_src,"rb") as f:

            img = f.read()

        temp_data = {"image":base64.b64encode(img)}

        temp_data = urllib.parse.urlencode(temp_data)

        # 发起http请求

        res = requests.post(self.url+"?access_token="+token,data=temp_data,headers=self.headers)


        # 判断识别结果元素个数

        if res.json()["words_result_num"] != 4:

            return {"errcode":1,"msg":"识别失败"}

        else:

            return {"errcode":0,"msg":"".join([x["words"] for x in res.json()["words_result"]])}






# 抽象类

class ThirdLogin(metaclass=ABCMeta):

    # 指定具体的方法，但是不实现方法内容

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_info(self,code):

        pass

    @abstractmethod
    async def check_user(self,name,avatar_url):

        pass

    @abstractmethod
    async def create_token(self,user):

        pass


# 封装手机号三方登录
class PhoneLogin:

    def __init__(self,phone):

        self.phone = phone


    # 生成token

    async def create_token(self,user):


        # 生成token

        token = Token().encode({"uid":user.id})

        # 生成refresh_token

        refresh_token = Token().encode({"uid":user.id})


        async with redis.client() as r:
            await r.set(refresh_token,user.id)


        return token,refresh_token


    # 封装判断手机账号方法

    async def check_user(self):

        try:

            user = await db.get(UserModel.select().where(UserModel.phone==self.phone))

        except Exception as e:

            # 自动注册功能

            # 动态入库

            user = await db.create(UserModel,username=self.phone,phone=self.phone,password="")


        return user





# 钉钉登录类
class DingdingLogin(ThirdLogin):

    def __init__(self):


        self.appid = "dingoaukgkwqknzjvamdqh"

        self.redirect_uri = "http://localhost:5000/dingding_back/"

    async def create_token(self,user):

        token = Token().encode({"uid":user.id})

        # 生成refresh_token

        refresh_token = Token().encode({"uid":user.id})


        async with redis.client() as r:
            await r.set(refresh_token,user.id)

        return token,refresh_token

    async def check_user(self,name):

        # 进行判断

        try:

            res = await db.get(UserModel.select().where(UserModel.username==name))

        except Exception as e:

            print(str(e))

            res = await db.create(UserModel,username=name,password="")


        return res

    # 获取用户信息
    def get_info(self,code):

        # 获取签名

        signature,timestamp =  self.sign()

        # 获取钉钉的标识：真实姓名

        res = requests.post(

            "https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature="+urllib.parse.quote(signature.decode("utf-8"))+"&timestamp="+timestamp+"&accessKey=dingoaukgkwqknzjvamdqh",

            data = json.dumps({"tmp_auth_code":code}),

            headers = {"Content-Type":"application/json"}


            )

        #print(res.text)

        # 获取用户信息

        user = res.json()["user_info"]["nick"]

        return user


    # 生成签名
    def sign(self):

        # 格式化时间戳
        timestamp = str(round(time.time() * 1000))

        # 密钥

        secret = "ly-AzMKMmCKQP3geaILT_An32kEfKO3HeOtApy5CgKwjytevVZC0WYsT2gxMB160"

        # 构造签名

        signature = base64.b64encode ( hmac.new(secret.encode("utf-8"),timestamp.encode("utf-8"),digestmod=hashlib.sha256).digest() )

        return signature,timestamp


    # 获取跳转的url
    def get_url(self):

        return f'https://oapi.dingtalk.com/connect/qrconnect?appid={self.appid}&response_type=code&scope=snsapi_login&state=STATE&redirect_uri={self.redirect_uri}'


# Gitee登录类
class GiteeLogin(ThirdLogin):

    def __init__(self):


        self.appid = "b54e3d3590627779968ccc78fe68c863ce7ccae01ed9925184880e95d5d1a5be"

        self.redirect_uri = "http://localhost:5000/gitee_back/"

        self.secret = "8e2a67cb4163a6528694c7d21645270a186f332ec1909662a7002fffafd4d45a"


    # 获取用户信息
    def get_info(self,code):

        # 换token

        res = requests.post(f"https://gitee.com/oauth/token?grant_type=authorization_code&code={code}&client_id={self.appid}&redirect_uri={self.redirect_uri}&client_secret={self.secret}")

        token = res.json()["access_token"]

        # 获取用户信息

        res = requests.get(f"https://gitee.com/api/v5/user?access_token={token}")

        name = res.json()["name"]

        avatar_url = res.json()["avatar_url"]

        return name,avatar_url

    # 判断用户账号

    async def check_user(self,name,avatar_url):

        # 进行判断

        try:

            res = await db.get(UserModel.select().where(UserModel.username==name))

        except Exception as e:

            print(str(e))

            res = await db.create(UserModel,username=name,password="",avatar=avatar_url)

        return res

    # 生成token

    async def create_token(self,user):

        # 生成token

        token = Token().encode({"uid":user.id})

        # 生成refresh_token

        refresh_token = Token().encode({"uid":user.id})


        async with redis.client() as r:
            await r.set(refresh_token,user.id)

        return token,refresh_token,user.avatar





    # 获取跳转的url
    def get_url(self):

        return f"https://gitee.com/oauth/authorize?client_id={self.appid}&redirect_uri={self.redirect_uri}&response_type=code"









# 添加一个工厂类
# 简单工厂类
class SimpleFactory:

    # 帮我们返回我们需要的实例

    # 返回需要的实例
    @staticmethod
    def get_object(name,phone=None):

        if name == "dingding":

            return DingdingLogin()

        elif name == "gitee":

            return GiteeLogin()

        elif name == "phone":

            return PhoneLogin(phone)




# 生成随机验证码

def create_code(abc=False,length=4):


    if abc:

        source = "0123456789qwertyuioplkjhgfdsazxvbnm"

    else:

        source = "0123456789"


    return "".join([random.choice(source) for _ in range(length)])

# 保存短信验证码

async def save_code(phone,code,lifetime=60):

    async with redis.client() as r:

        await r.set(f"{phone}_msg",code)

        # 过期时间

        await r.expire(f"{phone}_msg",lifetime)


# 构建钉钉机器人请求类

class Robot:

    def __init__(self):

        # 时间戳
        self.timestamp = ""

        # 密钥
        self.secret = "SEC6c4eb99c5369ba9a3c1f45ea3932bea0d93d02e39f45e70488e648a715432a3d"

        # 定义信息接口

        self.webhook = "https://oapi.dingtalk.com/robot/send?access_token=ceb02c44e776e8cca26fd4fc267b1d8fae4d55ab8663c7615ac101ad0c911025"
    # 发送短信
    def send(self,code,phone=None):

        # 构建信息结构

        data = {"msgtype":"text","text":{"content":code}}


        # 针对某一个人的信息发送机制

        if phone:

            data["at"] = {"atMobiles":[phone]}


        timestamp,mysign = self.sign()

        # 发送信息

        res = requests.post(self.webhook+f"&timestamp={timestamp}&sign={mysign}",data=json.dumps
        (data),headers={"Content-Type":"application/json"})

        print(res.text)



    # 生成签名

    def sign(self):

        # 获取签名时间的时间戳

        # 获取签名时的时间戳
        timestamp = str(round(time.time() * 1000))

        self.timestamp = timestamp

        # 密钥转码
        secret = self.secret.encode("utf-8")

        # 签名拼接
        sign_str = "{}\n{}".format(timestamp,self.secret)

        # 转码
        sign_str = sign_str.encode("utf-8")

        # 加密
        hmac_code = hmac.new(secret,sign_str,digestmod=hashlib.sha256).digest()

        # urlencode
        mysign = urllib.parse.quote(base64.b64encode(hmac_code))

        return timestamp,mysign









class CheckRe:


    def check_phone(self,phone):

        # match search

        return re.match(r"^1[3456789]\d{9}$",phone)








# 比对验证码

async def check_code(key,code):


    # 从redis里读取key的值

    async with redis.client() as r:

        redis_code = await r.get(key)


    if redis_code:

        if int(redis_code) == int(code):

            return True

        else:

            return False

    else:

        return False






# 随机取色
def get_random_color():

    return (random.randrange(255),random.randrange(255),random.randrange(255))


# 构建黑名单类库

class BlackManage:

    def __init__(self):

        # 初始化黑名单的key
        self.key = "black"

    # 添加黑名单

    async def add(self,username):


        # 获取所有黑名单列表
        async with redis.client() as r:

            blacklist = await r.lrange(self.key,0,-1)

            # 设置过期时间

            await r.set(f"{username}_{self.key}",1)

            await r.expire(f"{username}_{self.key}",30)

            if username not in blacklist:

                await r.lpush(self.key,username)

                


    # 移除黑名单

    async def rem(self,username):


        async with redis.client() as r:

            await r.lrem(self.key,1,username)








# 声明token类

class Token:

    def __init__(self):

        # 可逆对称加密算法
        self.secret = "123"


    # 加密

    def encode(self,data):


        return jwt.encode(data,self.secret,algorithm='HS256')


    # 带生命周期的token

    def encode_time(self,data,seconds=30):

        # 提前定义载荷信息

        playload = {

            "exp": int((datetime.datetime.now() + datetime.timedelta(seconds=seconds)).timestamp()),
            "data":data
        }

        return jwt.encode(playload,self.secret,algorithm='HS256')


    # j解密操作

    def decode(self,token):


        data = jwt.decode(token,self.secret,algorithms=["HS256"])

        return data


# 通用带参的装饰器
def check_role(role=4):

    def decorator(func):

        async def wrapper(self,*args,**kwargs):


            if self.rid & role == 0:


                return self.finish({"errcode":2,"msg":"您不具备该接口的权限"})


            await func(self,*args,**kwargs)


        return wrapper


    return decorator


# 检查是否是管理员
def check_admin(func):


    async def wrapper(self,*args,**kwargs):

        # 判断用户角色

        if self.rid & role_dict[2] == 0:

            return self.finish({"errcode":2,"msg":"您不是管理员"})


        await func(self,*args,**kwargs)




    return wrapper


# 检查token的装饰器

def check_token(func):

    async def wrapper(self,*args,**kwargs):


        # 接收参数token

        token = self.request.headers.get("token",None)

        if not token or token == "null":

            return self.finish({"errcode":1,"msg":"您的token不存在"})

        # 解码操作

        try:
            user = Token().decode(token)
        except Exception as e:
            return self.finish({"errcode":2,"msg":"您的token不合法"})


        # 上下文变量赋值

        print(user)

        self.uid = user["uid"]


        # 查询rid

        res = await db.get(UserModel.select().where(UserModel.id==self.uid))

        self.username = res.username

        self.rid = res.rid

        await func(self,*args,**kwargs)


    return wrapper




# if __name__ == '__main__':


    
#     #print( Token().encode_time({"uid":10}) )

#     #print(Token().decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODM1OTM0MjksImRhdGEiOnsidWlkIjoxMH19.vZL3u2IE929lbGvYAuWAChJDmSiY1uSC4GLPSTT6m2E"))


# 声明加密方法

def make_password(password,salt="zxczxczxc"):


    # 生成md5对象

    md5 = hashlib.md5()

    # 转码

    password_utf8 = str(password+salt).encode(encoding="utf-8")


    # 加密操作

    md5.update(password_utf8)


    return md5.hexdigest()


# 封装非空验证字段
field_list = {
    
    "username":{"errcode":1,"msg":"用户名不能为空"},
    "password":{"errcode":1,"msg":"密码不能为空"},
    "phone":{"errcode":1,"msg":"手机号不能为空"},
    "code":{"errcode":1,"msg":"验证码不能为空"},


}

# 非空验证方法

def check_none(fields):


    # 提前声明返回值

    res = None

    # 循环指定的参数列表

    for x in fields:

        # 判断是否为None

        if not x[1]:

            res = {"errcode":field_list[x[0]]["errcode"],"msg":field_list[x[0]]["msg"]}

            # 结束当前循环
            break


    return res


