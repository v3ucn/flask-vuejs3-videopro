import tornado.web

import json


from tornado import websocket

from utils.util import Token,check_token,TalkLog

from model.models import MsgModel,db,UserModel,redis

from playhouse.shortcuts import model_to_dict

from test.time_order import s_dict,send_user,release_user


# 存储链接对象

users = {}


# 创建websocket基础类

class WebSocket(websocket.WebSocketHandler):


    # 跨域
    def check_origin(self,origin):

        return True

    # 接收消息

    def on_message(self,message):

        print(message)

        self.write_message(message)


    # 开启链接

    async def open(self):

        # 获取token

        token = self.get_argument("token",None)

        if not token or token == "null":

            self.close(code=1002,reason="您未登录")

            return

        # 解密token

        try:

            user = Token().decode(token)

        except Exception as e:

            print(str(e))

            self.close(code=1002,reason="您的token不合法")

            return

        users[user["uid"]] = self

        # 用户又链接上websocket

        async with redis.client() as r:

            offline_user = await r.get("msg_7")


        offline_user = eval(offline_user)

        if user["uid"] in offline_user:

            self.write_message("推送刚才不在线的消息")



        print(users)

    # 断开
    def on_close(self):

        # 字典的遍历删除

        mykey = None

        for key,item in users.items():

            if item == self:

                mykey = key

        users.pop(mykey)

        print(f"{mykey}用户已经关闭websocket链接")



        # users.remove(self)





# 创建http协议基础类
class BaseHandler(tornado.web.RequestHandler):


    def __init__(self,*args,**kwargs):

        # 调用父类的初始化方法
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)


        # 子类调用父类方式  super方法
        # super(BaseHandler,self).__init__(*args,**kwargs)


    def options(self,*args):

        #设置状态吗
        self.set_status(204)
        self.finish()


    # 跨域

    def set_default_headers(self):

        # 请求来源
        self.set_header("Access-Control-Allow-Origin","*")

        # 请求方式
        self.set_header("Access-Control-Allow-Methods","POST,GET,PUT,DELETE,TRACE,HEAD,PATCH,OPTIONS")

        # 请求头
        self.set_header("Access-Control-Allow-Headers","*")


    # 重写父类 finish
    def finish(self,chunk=None):


        # 判断参数内容是否为None     判断参数类型是否为文件
        if chunk is not None and not isinstance(chunk,bytes):

            # 序列化
            chunk = json.dumps(chunk,indent=4,sort_keys=True,default=str,ensure_ascii=False)


        try:

            tornado.web.RequestHandler.write(self,chunk)

        except Exception as e:

            pass

        # 调用父类的finish

        tornado.web.RequestHandler.finish(self)


class Talk(BaseHandler):


    # 获取聊天记录
    @check_token
    async def get(self):

        to_uid = self.get_argument("to_uid",None)


        tl = TalkLog(self.uid,to_uid)

        msglist = await tl.get()


        self.finish({"errcode":0,"data":msglist})




    # 聊天推送
    @check_token
    async def post(self):

        # 获取聊天信息

        msg = self.get_argument("msg")

        # 获取聊天对象的uid

        to_uid = self.get_argument("to_uid",None)

        # 获取消息类型

        msg_type = self.get_argument("msg_type",1)



        if not to_uid:

            # 群聊

            for key,val in users.items():

                msg_dict = {"username":self.username,"msg":msg,"uid":self.uid}

                msg_dict = json.dumps(msg_dict,ensure_ascii=False)

                val.write_message(msg_dict)

        else:



            msg_dict = {"username":self.username,"msg":msg,"uid":self.uid,"msg_type":msg_type}

            msg_dict = json.dumps(msg_dict,ensure_ascii=False)

            users[int(to_uid)].write_message(msg_dict)

            users[int(self.uid)].write_message(msg_dict)


            tl = TalkLog(self.uid,to_uid)

            await tl.add(self.username,msg,self.uid,msg_type)



        
        self.finish({"errcode":0,"msg":"消息发送成功"})



# 客服

class Customer(BaseHandler):

    # 释放客服
    @check_token
    async def delete(self):


        # 获取要释放的客服的id

        uid = self.get_argument("uid",None)

        # 释放

        release_user(int(uid))


        self.finish({"errcode":0,"msg":"已经关闭客服聊天"})


    # 分配客服

    @check_token
    async def get(self):

        global s_dict


        # 查询所有客服

        customers = await db.execute(UserModel.raw("  select id,username from user where rid & 8 != 0  "))


        # 检查是否在线

        on_line_user = []

        for x in customers:

            for key in users.keys():

                if x.id == key:

                    on_line_user.append({"uid":x.id,"username":x.username})


        if not on_line_user:

            return self.finish({"errcode":1,"msg":"客服不在线"})



        # 确保容器内有客服

        uids = [x["uid"] for x in on_line_user]


        # 放入时序容器内

        s_dict[0] = uids


        # 分配客服

        cid = send_user(self.uid)


        username = [x["username"] for x in on_line_user if x["uid"] == cid]



        # 哈希取模算法

        # c_index = hash(self.uid) % len(on_line_user)


        self.finish({"errcode":0,"uid":cid,"username":username[0]})




class PushMsg(BaseHandler):


    async def post(self):


        # 消息内容
        msg = self.get_argument("msg")

        # 用户uid

        uid = self.get_argument("uid",None)


        # 消息内容存储

        res = await db.create(MsgModel,content=msg)

        print(res)


        # 在线用户uid

        uids = []



        if not uid:

            # 广播

            for key,val in users.items():

                val.write_message(msg)

                uids.append(str(key))


            uids = ",".join(uids)

            # 查询未在线用户

            offline_user = await db.execute(UserModel.raw(f" select id from user where id not in ({uids})  "))

            offline_user = [x.id for x in offline_user]

            async with redis.client() as r:

                await r.set(f"msg_{res}",str(offline_user))

            print(offline_user)






        else:

            # 精准推送

            val = users.get(int(uid),None)


            # 推送

            if val:

                val.write_message(msg)






        self.finish({"errcode":0,"msg":"消息推送成功"})