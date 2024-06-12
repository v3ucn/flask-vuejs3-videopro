# requests库进行接口测试

import requests


# 封装测试类


class ApiTest:


    # 初始化方法
    def __init__(self):

        # 定义测试接口地址

        self.url = "http://localhost:5000/"

        self.headers = {"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEwfQ.QlP6zDkRhgn0OFhgswG1BzNUs5WvyjjMbbp7HbVwwyc"}

        # self.headers = {}

        # 定义文件上传地址

        self.files = {"file":("test.mp4",open(r"C:\Users\zcxey\test.mp4","rb"))}


    def put(self,url,data={}):


        # 发起请求  http

        res = requests.put(f"{self.url}{url}",data=data,headers=self.headers)

        print(res.text)

    def get(self,url,data={}):

        # 发起请求

        res = requests.get(f"{self.url}{url}",params=data,headers=self.headers)

        print(res.text)

        return res.json()


    def delete(self,url,data={}):

        # 发起请求

        res = requests.delete(f"{self.url}{url}",params=data,headers=self.headers)

        print(res.text)

        return res.json()


    # 请求方法  post

    def post(self,url,data={}):


        # 发起请求  http

        res = requests.post(f"{self.url}{url}",data=data,headers=self.headers,files=self.files)

        print(res.text)


if __name__ == '__main__':
    
    # 实例化对象
    at = ApiTest()

    # 调用post方法

    #at.post("user/",{"username":"111","password":"111","phone":"111"})

    # 调用get方法

    res = at.get("customer/",{"msg":"这里是给17的私聊信息","to_uid":17})

    print(res)





