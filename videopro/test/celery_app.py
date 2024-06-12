# 异步任务队列

from celery import Celery


# 实例化对象

app = Celery("tornado")

# 定义异步任务的存储容器

app.conf.broker_url = "redis://localhost:6379"

app.conf.result_backend = "redis://localhost:6379"

# 定义时区

app.conf.timezone = "Asia/Shanghai"


# 定义消费任务  0-9

@app.task(name="tornado",property=1)
def job():

    print("执行异步任务队列的任务")