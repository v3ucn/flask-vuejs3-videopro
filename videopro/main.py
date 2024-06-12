# 导包
import tornado.web
import tornado.ioloop

import os

# 非同级目录进行导包

from app import base,user,role

from test.celery_app import job


# 声明静态目录

static_path = os.path.join(os.path.dirname(__file__),"static")




# 创建类试图

class HelloHandler(base.BaseHandler):

    async def get(self):

        # 调用celery的内置异步任务方法
        job.delay()

        self.finish({"msg":"你好世界"})


urlpatterns = [

(r'/',HelloHandler),
(r'/websocket/',base.WebSocket),
(r'/pushmsg/',base.PushMsg),
(r'/talk/',base.Talk),
(r'/customer/',base.Customer)

]


urlpatterns += ( user.urlpatterns + role.urlpatterns )



# 创建实例

app = tornado.web.Application(handlers=urlpatterns,debug=True,static_path=static_path)


# 启动服务

if __name__ == '__main__':


    print("服务正常启动")

    app.listen(5000)

    tornado.ioloop.IOLoop.instance().start()
    


