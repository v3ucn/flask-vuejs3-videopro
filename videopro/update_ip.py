import os
import subprocess
import sys

import locale



cmd = "netsh interface ip set address name=以太网 static 192.168.201.137 255.255.248.0 192.168.200.1"

#cmd = "netsh interface show interface"


p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    result = p.stdout.readline()  #默认获取到的是二进制内容
    if result != b'':  #获取内容不为空时
        try:
            print(result.decode('gbk').strip('\r\n'))  #处理GBK编码的输出，去掉结尾换行
        except:
            print(result.decode('utf-8').strip('\r\n'))  #如果GBK解码失败再尝试UTF-8解码
    else:
        break


