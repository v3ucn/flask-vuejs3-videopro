# 导包

# from flask import Flask,jsonify


# # 创建flask实例

# app = Flask(__name__)

# # 配置禁止转码

# app.config["JSON_AS_ASCII"] = False


# # 视图逻辑

# @app.route("/",methods=['GET','POST'])
# def hello_world():

#     return jsonify({"msg":"你好世界"})


class A:

    def __init__(self,a1):

        print(f"我是A的初始化方法{a1}")

    def finish(self):

        print("123123")


class B(A):

    def __init__(self,*args):

        # 调用一下父类的初始化方法
        A.__init__(self,*args)

        print("我是B的初始化方法")

    def test(self):

        self.finish()

        print("test")


# 启动服务

if __name__ == '__main__':
    

    B((1,)).test()