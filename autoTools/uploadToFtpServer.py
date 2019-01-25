#-*-coding:utf-8-*-
import os
import ftplib
import paramiko
import sys

class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host, port=21):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    # def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
    #     file_handler = open(LocalFile, 'wb')
    #     print(file_handler)
    #
    #     self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 接收服务器上文件并写入本地文件
    #     file_handler.close()
    #     return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)  # 上传文件
        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False
        print("LocalDir:", LocalDir)
        LocalNames = os.listdir(LocalDir)
        print("list:", LocalNames)
        print(RemoteDir)

        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print
        "remoteDir:", RemoteDir
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print
        "RemoteNames", RemoteNames
        print
        self.ftp.nlst("/del1")
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

def sshexecute(serverIp, cmd):
    try:
        # 创建ssh客户端
        client = paramiko.SSHClient()
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(serverIp, 22, username="ute", password="ute", timeout=20)
        # 执行命令
        print "begin to execute the cmd:" + cmd
        stdin, stdout, stderr = client.exec_command(cmd)  # 远程执行shell命令
        print(stdout.readlines())  # 输出回显结果
    except Exception, e:
        print e
    finally:
        client.close()

if __name__ == "__main__":

    ftpFilePath = "/CSV/YSQ/"

    # if len(sys.argv[0]) > 1:
    #     targetpath = sys.argv[1]
    #     fileName = targetpath.split("/")[-1]
    # else:

    targetpath = "/home/ute/robotlte/LTE4537/log/"

    fileList = os.listdir(targetpath)
    floderList = []
    for p in fileList:
        if os.path.isdir(targetpath + p) == True:
            floderList.append(p)
    floderList = sorted(floderList, key=lambda x: os.path.getmtime(os.path.join(targetpath, x)))
    targetpath = targetpath + floderList[-1]
    fileName = floderList[-1] + ".zip"

    print "start to zip floder" + fileName
    cmd = "cd " + targetpath + "; zip -r " + fileName +" ./*"
    sshexecute("10.108.183.152",cmd)

    print "start to upload floder" + fileName
    ftp = myFtp('10.56.6.5')
    ftp.Login('tdlte', 'tdlte')  # 登录，如果匿名登录则用空串代替即可
    ftp.UpLoadFile(targetpath + fileName, ftpFilePath + fileName)
    ftp.close()

    cmd = "cd " + targetpath + "; rm " + fileName
    sshexecute("10.108.183.152",cmd)













