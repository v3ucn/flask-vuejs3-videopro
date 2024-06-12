# 定时任务

import time

from datetime import datetime

from apscheduler.schedulers.tornado import TornadoScheduler

from tornado.ioloop import IOLoop

from tornado import web

import asyncio


# 设置模块的路径

import os,sys

# # 设置基础路径

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载项目路径

sys.path.append(base_path)

# 加载指定模块

sys.path.append(os.path.join(base_path,'model'))


from model.models import redis as redis_async

# 任务持久化

from apscheduler.jobstores.redis import RedisJobStore


# 设置任务仓库

jobstores = {
        
        "default":RedisJobStore(jobs_key="cron.jobs",run_times_key="cron.run_times",host="localhost",port=6379,)


}


scheduler = None


async def job(vid):

    _now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 判断该视频是否完成了审核

    # 获取确认队列

    async with redis_async.client() as r:

        confirm_job = await r.lrange("confirm_job",0,-1)


    print(confirm_job)

    # 兼容加权和非加权

    for x in confirm_job:

        if isinstance(x,str):

            # 加权队列

            x = eval(x)

            if x[0] == vid:

                print("该审核任务有问题，超时了")

        else:

            if x == vid:

                print("该审核任务有问题，超时了")


    print(f"定时执行:{_now}")


    # 删除定时任务

    #scheduler.remove_job(f"job_{vid}")







# 定义定时执行实例对象

def init_scheduler(vid):

    global scheduler

    scheduler = TornadoScheduler(jobstores=jobstores)

    scheduler.start()

    # 添加异步定时任务

    scheduler.add_job(job,"interval",seconds=10,id=f"job_{vid}",args=(vid,))

    print("定时任务开始执行")

if __name__ == '__main__':
    
    init_scheduler(2)

    app = web.Application([],debug=True)

    app.listen(8888)

    IOLoop.current().start()