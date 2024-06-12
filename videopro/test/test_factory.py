# 简单工厂模式

class DingdingLogin:

    def __init__(self):


        self.appid = "dingoaukgkwqknzjvamdqh"

        self.redirect_uri = "http://localhost:5000/dingding_back/"


    # 获取跳转的url
    def get_url(self):

        return f'https://oapi.dingtalk.com/connect/qrconnect?appid={self.appid}&response_type=code&scope=snsapi_login&state=STATE&redirect_uri={self.redirect_uri}'

        


class Gitee:

    def __repr__(self):

        return "Gitee登录"


# 添加一个工厂类
# 简单工厂类
class SimpleFactory:

    # 帮我们返回我们需要的实例

    # 返回需要的实例
    @staticmethod
    def get_object(name):

        if name == "dingding":

            return DingdingLogin()

        elif name == "gitee":

            return Gitee()




if __name__ == '__main__':
    
    print(SimpleFactory.get_object("dingding").get_url())