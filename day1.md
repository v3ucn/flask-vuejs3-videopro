# 确保本机Python大版本不低于3.9，可以正常运行

# 确保前端安装pnpm框架

# 安装Tornado异步框架

# Git已经安装

# 确保建立以自己名字命名的分支

# 软件  数据库：Mysql redis  可视化：navicat  压测工具:xampp

# 拉取前端vue3.0项目,并且能够正常运行  https://gitee.com/QiHanXiBei/vue3

# Tornado  三大框架  异步非阻塞  性能高  每秒处理1000个请求  降本增效

# Django 500个请求 2台服务器  Tornado  1台服务器

# 视频社交平台  videosite

# 建立平台数据库  create database edu default character set utf8mb4 collate utf8mb4_unicode_ci;

# ORM模块  pip install peewee peewee_async

# 项目依赖文件  requerements.txt  依赖列表

# 基类表  主键  创建时间   面向对象 继承性

# 项目模块化  模仿django目录结构  添加 .gitignore

# 两种导包方式：相对路径： from 文件 import 具体库  sys.path.append("..")

# 系统化模块导包

# 设置模块路径
import os,sys

# 设置根路径

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加模块路径
sys.path.append(base_path)
sys.path.append(os.path.join(base_path,'config'))

# 声明用户视图 user.py  注册接口 UserHandler  

# git命令

# 查看当前分支:git branch

# 切换分支:git checkout 分支名称

# 查看所有分支：git branch -a

# 建立分支: git checkout -b 分支名称

# 推送新分支 ： git push --set-upstream origin 分支名称

# 删除本地分支：git branch -d 分支名称

# 推送删除分支： git push origin --delete 新建名称

# 提交代码：  1 git add -A  2 git commit -M 3 git push origin 分支名

# 项目内导包： from 模块名.文件名 import 类/方法/属性

# 编码和跨域功能，通过继承进行重写操作，注意函数名是否和父类重复

# restful风格  使用名词  提高复用性 减少接口复杂度

# 完成自动化测试脚本，添加其他的实例方法

# 不查询来去重

# 构造注册页面

# 异步调用  原生异步关键字  async 声明异步方法  await 调用异步方法

# 非阻塞特性：同步阻塞机制，排队，一个一个执行，切换，底层回调函数

# 加密算法：密码学的范畴，两大分类：对称加密和非对称加密，对称加密：加密和解密的密钥是一致的，可逆和不可逆

# jwt json-web-token  token:三部分，头部，载荷，密钥

# 登录成功->调用jwt类->生成用户token->将参数和token返回前端->前端本地存储->跳转首页->欢迎当前登录用户名->退出功能

# 涉及IO操作  引起阻塞    文件读写  数据库读写/内存读写  网络请求

# 原子操作 要么都执行，要么都不执行

# 给token设置生命周期  增加refress_token  换取gitee用户信息

# 索引  唯一索引 单列唯一索引  联合唯一索引

# 因子登录 系统安全性 用户数据安全  单因子：账号和密码  双因子：客户端设备认证

# get和post区别，浏览器限制url

# 播放次数  一定要放在redis   热数据(读写次数频繁)：redis  冷数据:mysql(innodb/myisam)

# 外键  逻辑外键/物理外键  逻辑删除/物理删除

# 调试 debug   断点调式