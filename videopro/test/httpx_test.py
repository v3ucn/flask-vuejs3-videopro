import asyncio

import httpx


# 封装请求类

class Request:


    def __init__(self):


        # 定义测试接口地址

        self.url = "http://localhost:5000/"

        self.headers = {"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEwfQ.QlP6zDkRhgn0OFhgswG1BzNUs5WvyjjMbbp7HbVwwyc"}

        # self.headers = {}

        # 定义文件上传地址

        self.files = {"file":("test.mp4",open(r"C:\Users\zcxey\test.mp4","rb"))}


    async def post(self,url,data={}):


        # 异步上下文管理器
        async with httpx.AsyncClient() as client:

            # 发起异步请求

            res = await client.post(f"{self.url}{url}",data=data,headers=self.headers,files=self.files)

            print(res.text)


if __name__ == '__main__':
    
    asyncio.run(Request().post("upload/",{"upload_type":"video"}))