# 多任务消费

import time

import threading

from multiprocessing import Process

import asyncio


async def job(num):

    print(f"执行任务{num}")

    await asyncio.sleep(1)


def main(num):

    asyncio.run(job(num))



if __name__ == '__main__':

    # 启动协程任务

    # asyncio.run(main())


    
    # 创建多线程对象

    threads = [threading.Thread(target=main,args=(x,)) for x in range(4)]

    # 创建多进程对象

    #threads = [Process(target=job,args=(x,)) for x in range(10)]

    # 启动多线程

    [x.start() for x in threads]

    # 阻塞主线程

    [x.join() for x in threads]

