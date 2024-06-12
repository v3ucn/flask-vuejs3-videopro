# 函数嵌套  内函数对外函数的变量进行引用  闭包

# 判断原则


# 1 必须有嵌套函数

# 2 内函数必须引用外函数的变量

# 3 外函数的返回值必须是内函数

from functools import wraps


def my_decorator(func):

    @wraps(func)
    def wrapper():

        # 添加一些逻辑
        print("装饰器被调用了")
        func()

        print("逻辑执行以后，也可以附加功能")

    return wrapper


# 带参的装饰器

def my_decorator(num=1):

    def decorator(func):

        def wrapper():

            print(num)

            func()

        return wrapper

    return decorator



@my_decorator(num=10)
def test():

    print("上传接口")


if __name__ == '__main__':
    
    test()

