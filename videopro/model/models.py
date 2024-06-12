# 导包

import peewee
import peewee_async


from datetime import datetime

import aioredis

import asyncio


# 创建数据库的链接对象

database = peewee_async.PooledMySQLDatabase("videopro",host="localhost",port=3306,user='root',password='root')


# 异步mysql数据库对象

db = peewee_async.Manager(database)

# 异步redis数据库对象

redis = aioredis.from_url("redis://localhost",encoding="utf-8",decode_responses=True)


# 基础模型类

class BaseModel(peewee.Model):

    # 主键
    id = peewee.IntegerField(primary_key=True,unique=True,constraints=[peewee.SQL("AUTO_INCREMENT")])

    # 创建时间
    create_time = peewee.DateTimeField(default=datetime.now)

    # 数据库链接和具体数据库类绑定
    class Meta:

        database = database


# 用户表

class UserModel(BaseModel):

    # 用户名
    username = peewee.CharField(max_length=100,null=False,unique=True)


    # 密码
    password = peewee.CharField(max_length=100,null=False)

    # 手机号
    phone = peewee.CharField(max_length=100,unique=True,null=True)


    # 用户头像
    avatar = peewee.CharField(max_length=100,null=True)


    # 角色id

    rid = peewee.IntegerField(default=1)


    # 数据库链接和具体数据库类绑定
    class Meta:

        # 声明表名
        db_table = "user"


# 视频表
class VideoModel(BaseModel):

    # 视频文件
    src = peewee.CharField(max_length=100,null=True)

    # 状态  1 通过审核  2 审核拒绝

    state = peewee.IntegerField(default=0)

    # 审核员id

    audit_id = peewee.IntegerField()

    # 发布人id

    uid = peewee.IntegerField()


    class Meta:

        db_table = "video"


# 消息表
class MsgModel(BaseModel):


    # 视频文件
    content = peewee.CharField(max_length=100,null=True)

    class Meta:

        db_table = "msg"



# 角色表
class RoleModel(BaseModel):

    # 角色名称
    name = peewee.CharField(max_length=100,null=False,unique=True)


    class Meta:

        db_table = "role"


# 用户_角色表

class UserRoleModel(BaseModel):


    # 用户id

    uid = peewee.IntegerField()

    # 角色id

    rid = peewee.IntegerField()


    class Meta:

        db_table = "user_role"






# 异步操作方法

async def main():

    async with redis.client() as r:

        await r.set("111","123")

        # 读取数据内容

        res = await r.get("111")


        print(res)


if __name__ == '__main__':


    # 当异步方法没有出现在tornado的异步视图内时，单独调用异步方法需要通过asyncio.run来进行调用

    #asyncio.run(main())

    
    # 数据库迁移

    # 创建表

    MsgModel.create_table(True)


    # 创建数据

    #res = VideoModel.create(src="test.mp4",uid=10)
    #res = VideoModel.create(src="test.mp4",uid=10)
    #res = VideoModel.create(src="test.mp4",uid=10)
    #res = RoleModel.create(name="管理员")

    # print(res.id)


    # 删除数据

    # UserModel.delete().where(UserModel.id == 3).execute()

    # 修改

    #res = UserModel.get(id=4)

    #res.username = "33333"

    #res.save()

    # 删除表

    #UserModel.drop_table(True)

