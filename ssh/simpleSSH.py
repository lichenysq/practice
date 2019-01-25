#-*-coding:utf-8-*-
import paramiko
from threading import Thread
import time
import json


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

username = "ute"
password = "ute"


def mutiThreadRunsSync(serverlist, cmdDict):
    threads = []
    for i in range(len(serverlist)):
        t = Thread(target=sshexecute, args=(serverlist[i], cmdDict.get(serverlist[i])),)
        threads.append(t)
    for i in range(len(serverlist)):
        threads[i].start()
    for i in range(len(serverlist)):
        threads[i].join()


@async
def mutiThreadRunAsync(serverlist, cmdDict):
    threads = []
    for i in range(len(serverlist)):
        t = Thread(target=sshexecute, args=(serverlist[i], cmdDict.get(serverlist[i])),)
        threads.append(t)
    for i in range(len(serverlist)):
        threads[i].start()
    for i in range(len(serverlist)):
        threads[i].join()

def sshexecute(ip,cmd):
    try:
        # # # #创建ssh客户端
        client = paramiko.SSHClient()
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(ip, 22, username=username, password=password, timeout=20)
        # 执行命令
        print(ip + ": begin to execute the cmd:" + cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        outstring = str(stdout.readlines())
        # print(outstring)
        if len(stderr.readlines()) < 1:
            print(ip + ": ****** success to execute the cmd:" + cmd)
        else:
            print(ip + ": ****** fail to execute the cmd:" + cmd)
            print(ip + "**** err mesg ****: " + str(stderr.readlines()))

    except Exception, e:
        print e
    finally:
        client.close()

@async
def sshexecuteAsync(ip,cmd):
    try:
        # # # #创建ssh客户端
        client = paramiko.SSHClient()
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(ip, 22, username=username, password=password, timeout=20)
        # 执行命令
        print(ip + ": begin to execute the cmd:" + cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        outstring = str(stdout.readlines())
        # print(outstring)
        if len(stderr.readlines()) < 1:
            print(ip + ": ****** success to execute the cmd:" + cmd)
        else:
            print(ip + ": ****** fail to execute the cmd:" + cmd)
            print(ip + "**** err mesg ****: " + str(stderr.readlines()))

    except Exception, e:
        print e
    finally:
        client.close()


def executeCmdsMultithreadAsync(dict):
    iplist = []
    for key in dict:
        iplist.append(key)
        mutiThreadRunAsync(iplist, dict)
    return("ok")


def executeCmdsMultithreadSync(dict):
    iplist = []
    for key in dict:
        iplist.append(key)
        mutiThreadRunsSync(iplist, dict)
    return("ok")

if __name__ == "__main__":
    #kong

    pass
