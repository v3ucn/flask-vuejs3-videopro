# 自动化脚本

from playwright.sync_api import sync_playwright

import time


# 设置模块的路径

import os,sys

# # 设置基础路径

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载项目路径

sys.path.append(base_path)

# 加载指定模块

sys.path.append(os.path.join(base_path,'utils'))


from utils.util import BaiduAi



# 容错重试方法

def retry(func,token,img_src):


    success = False

    num = 0

    while not success and num < 3:

        res = func(token,img_src)

        if res["errcode"]:

            success = True

        num += 1

    return res


class Browser:



    # 登录流程
    def login(self,url):

        # 启动浏览器

        with sync_playwright() as p:

            browser = p.chromium.launch(channel="msedge",headless=False)

            # 新开一个页面

            page = browser.new_page()


            # 输入网址

            page.goto(url)

            time.sleep(2)


            # 输入表单

            page.get_by_placeholder("请输入用户名").fill("111")

            page.get_by_placeholder("请输入密码").fill("111")

            # 点击生成验证码按钮

            page.get_by_role("button",name="生成验证码").click()

            time.sleep(2)

            # 定位验证码图片

            page.get_by_role("img").screenshot(path="./test.png")

            # 实例化智能识图
            ba = BaiduAi()

            token = ba.get_token()

            #print(ba.check_img(token,r"./test.png"))


            code = retry(ba.check_img,token,r"./test.png")["msg"]


            # 回填验证码

            page.get_by_placeholder("请输入验证码").fill(code)



            page.get_by_role("button",name="登 录").click()
            



            time.sleep(10)





    # 注册流程

    def reg(self,url):


        # 启动浏览器

        with sync_playwright() as p:

            browser = p.chromium.launch(channel="msedge",headless=False)

            # 新开一个页面

            page = browser.new_page()


            # 输入网址

            page.goto(url)

            time.sleep(2)

            # 进行页面元素匹配

            page.get_by_placeholder("请输入用户名").fill("666")

            page.get_by_placeholder("请输入密码").fill("666")

            page.get_by_placeholder("请输入手机号").fill("666")

            # 点击提交按钮

            page.get_by_role("button",name="提 交").click()


            time.sleep(10)


    def start(self):


        # 启动浏览器

        with sync_playwright() as p:

            


            # 新开一个页面

            page = browser.new_page()

            # 输入网址

            page.goto(self.url)


            # 打印当前用户访问页面截图

            page.screenshot(path="./test.png")

            time.sleep(5)



# 任务方法

def test():

    print("执行某种任务")

    return True






if __name__ == '__main__':


    #retry(test)

    
    Browser().login("http://localhost:8080/login")

    



