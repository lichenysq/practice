#-*-coding:utf-8-*-
import paramiko
import threading
import os
import urllib
import datetime
from robot.api import logger
import re
from selenium import webdriver
import time

username = "ute"
password = "ute"
servdict = {}

global baseip
global flodername
global iphyServList

cmds = {}
cmds["scpBuild"] = "cd /home/ute; scp ute@#baseip#:/home/ute/Downloads/#buildName# ./Downloads"
cmds["yaft"] = "cd /home/ute/Downloads/trunk; echo \"oZPS0POrRieRtu\" | python yaft.py -i #enb_ip# -z ../#buildName# -R --ask_for_password"
cmds["checkYAFTisReady"] = "[ -f /home/ute/Downloads/trunk/yaft.py ] && echo \"exist\" || echo \"notexist\""


cmds["mkdir4iphy"] = "cd /opt/iphy; mkdir #flodername#"
cmds["scpWTS"] = "cd /opt/iphy/; scp -r ute@#baseip#:/opt/iphy/#flodername# ."
cmds["updateiphy"] = "cd /opt/iphy/; rm -rf latest; ln -sf #flodername# latest; cd latest;" \
                     "python fsmf_sw_update.py -i 192.168.200.#iphyID# --password oZPS0POrRieRtu --set_ge_ips 10.0.2.3#iphyID# 10.0.2.1 --set_log_ip 192.168.200.126 --set_fsm_id #iphyID# --set_srio_domain #iphyID# --save_iphy_xml"
cmds["killoldlua"] = "sudo pkill edaemon; sudo pkill egate"

cmds["rmoldpstool"] = "cd /home/ute/Downloads/; rm pstool*"




class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def mutiThreadRun(serverlist, cmd):
    threads = []
    for i in range(len(serverlist)):
        t = MyThread(sshexecute, args=(serverlist[i], cmd))
        threads.append(t)
        t.start()

    for i in range(len(serverlist)):
        threads[i].join()

    for item in threads:
        result = item.get_result()
        if "failed" == result:
            raise Exception("error, please check the log.html")

def sshexecute(ip,cmdindex):
    outstring = None
    try:
        client = paramiko.SSHClient()

        global baseip
        cmd = cmds.get(cmdindex).replace("#baseip#", baseip).replace("#flodername#", flodername)

        if servdict.get(ip) != None:
            cmd = cmd.replace("#buildName#", servdict.get(ip).split(";")[1]).replace("#enb_ip#", servdict.get(ip).split(";")[0])

        if cmdindex == "updateiphy":
            iphyID = str(iphyServList.index(ip) + 1)
            cmd = cmd.replace("#iphyID#", iphyID)


        #创建ssh客户端
         # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(ip, 22, username=username, password=password, timeout=20)
        # 执行命令
        print(ip + ": begin to execute the cmd:" + cmd)

        stdin, stdout, stderr = client.exec_command(cmd)
        outstring = str(stdout.readlines())

        if len(stderr.readlines()) < 1:
            pass
            # print(ip + ": ****** success to execute the cmd:" + cmd)
        else:
            logger.error(ip + "****** fail to execute the cmd:" + cmd, html=True)
    except Exception, e:
        print e

    finally:
        client.close()

        if "checkYAFTisReady" == cmdindex or "checkPackageisReady" == cmdindex:
            return outstring

        if "yaft" == cmdindex:
            now_time = datetime.datetime.now()
            logger.info(ip + ": yaft end at " + str(now_time), html=True)

            if "Flashing done" in outstring:
                print(ip + " *********  update enb successful *********")
            else:
                print("*********  YAFT update enb failed *********: " + ip)
                print(ip + ": failed details：" + outstring)
                return "failed"


def checkYAFTisReady(pciplist):
    temp = []
    for pcip in pciplist:
        result = sshexecute(pcip, "checkYAFTisReady").replace(" ","")
        if "notexist" in result:
            temp.append(pcip)

    if len(temp) > 0:
        logger.error("yaft not exist,  please checkout YAFT(https://svne1.access.nsn.com/isource/svnroot/BTS_T_YAFT/trunk) at /home/ute/Downloads/  first", html=True)
        # checkoutYAFT()
        raise Exception("YAFT not ready")

def updateEnb(input):
    global flodername
    flodername = "undefined"

    global baseip
    baseip = input[0].replace(" ", "").split(";")[0]

    packageSet = set()
    for item in input:
        valuelist = item.replace(" ", "").split(";")
        pcip = valuelist[0]
        enbip = valuelist[1]
        packageName = valuelist[2]
        packageSet.add(packageName)
        servdict[pcip] = enbip + ";" + packageName + "_release_BTSSM_downloadable.zip"

    logger.info("input info:" + str(servdict), html=True)

    for packitem in packageSet:
        zipfilename = packitem + "_release_BTSSM_downloadable.zip"

        cmds["checkPackageisReady"] = "[ -f /home/ute/Downloads/" + zipfilename + " ] && echo \"exist\" || echo \"notexist\""
        result = sshexecute(baseip, "checkPackageisReady").replace(" ","")

        if "notexist" in result:
            try:
                logger.info("begin to download:" + zipfilename, html=True)
                url = 'http://files.ute.inside.nsn.com/builds/enb/base/' + packitem + "/" + zipfilename
                urllib.urlretrieve(url, "/home/ute/Downloads/" + zipfilename)
                # fsize = os.path.getsize("/home/ute/Downloads/FL00_FSM4_9999_190212_024890_release_BTSSM_downloadable.zip")
            except Exception as e:
                print("download failed：" + zipfilename)
                print(e)
            else:
                print("file already exist, no need to download:" + str(zipfilename))




    allServList = []
    for key in servdict:
        allServList.append(key)

    checkYAFTisReady(allServList)

    logger.info('Info:begin to scp package', html=True)
    mutiThreadRun(allServList, "scpBuild")
    logger.info('Info:end to scp package', html=True)

    logger.info('Info:begin to execute YAFT', html=True)
    mutiThreadRun(allServList, "yaft")
    logger.info('Info:end to execute YAFT', html=True)

def uploadIphy(iphyinput, version=None):
    global iphyServList
    iphyServList = iphyinput
    global baseip
    baseip = iphyinput[0]

    f = urllib.urlopen('http://files.ute.nsn-rdnet.net/builds/wts/latestStable/')
    data = f.read()
    print(data.decode('utf-8'))
    zipfile = re.findall(r'href="\S*?zip\b', data)[0].replace("href=\"", "")
    tarfile = re.findall(r'href="\S*?core2.tar.bz2\b', data)[0].replace("href=\"", "")
    print(zipfile)
    print(tarfile)
    global flodername
    flodername = tarfile.split("_core")[0]


    if os.path.isfile('/opt/iphy/' + flodername + "/" + zipfile):
        logger.info("file already exist, no need to download:" + str(zipfile), html=True)
    else:
        mutiThreadRun(iphyServList, "mkdir4iphy")
        try:
            logger.info("begin to download:" + zipfile, html=True)
            if version == None:
                version = "latestStable"

            url = 'http://files.ute.nsn-rdnet.net/builds/wts/' + version + "/" + zipfile
            logger.info("zip url:" + url, html=True)
            urllib.urlretrieve(url, "/opt/iphy/" + flodername + "/" + zipfile)
            url = 'http://files.ute.nsn-rdnet.net/builds/wts/' + version + "/" + tarfile
            logger.info("tar url:" + url, html=True)
            urllib.urlretrieve(url, "/opt/iphy/" + flodername + "/" + tarfile)

            cmds["tariphy"] = "cd /opt/iphy/" + flodername + ";chmod 755 *; tar -xvf " + tarfile
            cmds["unzipiphy"] = "cd /opt/iphy/" + flodername + "; unzip " + zipfile
            sshexecute("127.0.0.1", "tariphy")
            sshexecute("127.0.0.1", "unzipiphy")

        except Exception as e:
            logger.info("download iphy failed：" , html=True)
            logger.info(e, html=True)


    mutiThreadRun(iphyServList, "scpWTS")
    print(iphyServList)
    mutiThreadRun(iphyServList, "updateiphy")
    sshexecute(iphyServList[0], "killoldlua")


def updateTtiTrace(input):
    global flodername
    flodername = "undefined"
    global baseip
    baseip = input[0].replace(" ", "").split(";")[0]

    packageSet = set()
    for item in input:
        valuelist = item.replace(" ", "").split(";")
        pcip = valuelist[0]
        enbip = valuelist[1]
        packageName = valuelist[2]
        packageSet.add(packageName)
        servdict[pcip] = enbip + ";" + packageName + "_release_BTSSM_downloadable.zip"

    for packitem in packageSet:
        try:
            logger.info("begin to download ttitrac")
            if packitem.startswith("FL"):
                url = 'http://files.ute.inside.nsn.com/builds/enb/base/' + packitem + "/TtiTracer.zip"
                urllib.urlretrieve(url, "/opt/TtiTracer/TtiTracer.zip")
            if packitem.startswith("TL"):
                if os.path.isfile('/home/ute/Downloads/pstools.zip'):
                    sshexecute("127.0.0.1", "rmoldpstool")
                driver = webdriver.Chrome()
                url = 'http://files.ute.inside.nsn.com/builds/enb/base/' + packitem + "/pstools.zip"
                driver.get(url)
                time.sleep(90)
                driver.close()
                # urllib.urlretrieve(url, "/home/ute/Downloads/pstools.zip ")
        except Exception as e:
            print("download ttitrace failed")
            print(e)

    for item in input:
        valuelist = item.replace(" ", "").split(";")
        pcip = valuelist[0]
        packageName = valuelist[2]

        if packageName.startswith("FL"):
            cmds["scpTtitrace"] = "scp ute@" + baseip + ":/opt/TtiTracer/TtiTracer.zip /opt/TtiTracer/"
            cmds["unzipTtitrace"] = "cd /opt/TtiTracer; rm -rf TtiTracer; unzip TtiTracer.zip"
            sshexecute(pcip, "scpTtitrace")
            sshexecute(pcip, "unzipTtitrace")
        if packageName.startswith("TL"):
            cmds["scpTtitrace"] = "scp ute@" + baseip + ":/home/ute/Downloads/pstools.zip  /opt/TtiTracer/"
            cmds["unzipTtitrace"] = "cd /opt/TtiTracer; rm -rf pstools; unzip pstools.zip"
            sshexecute(pcip, "scpTtitrace")
            sshexecute(pcip, "unzipTtitrace")


if __name__ == "__main__":
    pass
    # data = [u'10.108.183.152', u'10.108.183.156', u'10.108.183.182', u'10.108.183.158']
    # uploadIphy(data)


