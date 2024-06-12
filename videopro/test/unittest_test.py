# 单元测试  单测

# 目的：让程序尽量不出现bug


# 单元测试框架

import unittest


from requests_test import ApiTest



# 计算器

class Count:


    def __init__(self,a,b):

        self.a = int(a)

        self.b = int(b)


    # 加法

    def add(self):

        return self.a + self.b


# 测试用例  可能出现的情况，用用例的方式进行记录


# 测试用例类

class TestCount(unittest.TestCase):


    # 用例初始化方法
    def setUp(self):

        print("用例启动")

    # 编写用例

    def test_add(self):

        res = Count(2,3)

        # 比对结果

        # 实际结果和期望结果
        self.assertEqual(res.add(),5)


    # 测试结束调用方法

    def tearDown(self):

        print("用例结束")


# 登录接口测试用例


# 用例写法  用户名  密码

# 登录成功  用户名 和 密码 都合法  查询校验也成功   username:111   password:111  期望结果:登录成功

# 登录失败  用户名为空   密码合法   password:111   期望结果：用户名不能为空

# 登录失败  用户名合法   密码为空   username:111   期望结果：密码不能为空

# 登录失败  用户名为空   密码为空      期望结果：用户名不能为空

# 登录失败  username:123  password:444     期望结果：您的账号或者密码有误

# 登录失败  用户名空字符串   密码合法   username:"" password:111   期望结果：用户名不能为空

# 登录失败  用户名合法   密码空字符串   username:111 password:""  期望结果：密码不能为空

class TestLogin(unittest.TestCase):


    def setUp(self):

        # 初始化请求类

        # 实例化对象
        at = ApiTest()

        # 赋值给当前实例对象
        self.at = at


    def test_login_1(self):

        # 登录成功

        res = self.at.get("user/",{"username":"111","password":"111"})

        # 比对结果

        # 实际结果和期望结果
        self.assertEqual(res["msg"],"登录成功")

    def test_login_2(self):

        # 登录失败

        res = self.at.get("user/",{"password":"111"})

        # 比对结果

        # 实际结果和期望结果
        self.assertEqual(res["msg"],"用户名不能为空")






if __name__ == '__main__':
    
    # 构造测试集

    suite = unittest.TestSuite()
    suite.addTest(TestLogin("test_login_1"))
    suite.addTest(TestLogin("test_login_2"))

    # 测试
    runner = unittest.TextTestRunner()
    runner.run(suite)