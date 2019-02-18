#-*-coding:utf-8-*-
import paramiko
import threading


# TL00_FSM4_9999_181129_000699_release_BTSSM_downloadable
# FL00_FSM4_9999_181128_023560_release_BTSSM_downloadable
servdict = {}
# servdict["10.108.183.152"] = "192.168.255.1;FL00_FSM4_9999_190212_024890_release_BTSSM_downloadable.zip"
# servdict["10.108.183.160"] = "192.168.255.7;FL00_FSM4_9999_190212_024890_release_BTSSM_downloadable.zip"
# servdict["10.108.183.156"] = "192.168.255.1;FL00_FSM4_9999_190118_024487_release_BTSSM_downloadable.zip"
# servdict["10.108.183.162"] = "192.168.255.7;FL18A_ENB_0000_000692_000000_release_BTSSM_downloadable.zip"

# servdict["10.108.183.182"] = "192.168.255.1;TL00_FSM4_9999_190119_000198_release_BTSSM_downloadable.zip"
# servdict["10.108.183.161"] = "192.168.255.7;TL18A_ENB_0000_000447_000000_release_BTSSM_downloadable.zip"
servdict["10.108.183.158"] = "192.168.255.1;TL00_FSM4_9999_190212_000196_release_BTSSM_downloadable.zip"
servdict["10.108.183.163"] = "192.168.255.7;TL00_FSM4_9999_190212_000196_release_BTSSM_downloadable.zip"


baseip = "10.108.183.152"
iphyName = "1901_709445.2"
# 按顺序
iphyServList = ["10.108.183.152", "10.108.183.156", "10.108.183.182", "10.108.183.158"]

cmds = {}
cmds["cleanlog"] = "cd /home/ute/robotlte/LTE4537/log/; rm -r *"

cmds["scpBuild"] = "cd /home/ute; scp ute@#baseip#:/home/ute/Downloads/#buildName# ./Downloads"
# cmds["unzipBuild"] = "cd /home/ute/Downloads; unzip #buildName#.zip -d #buildName#"
cmds["yaft"] = "cd /home/ute/Downloads/YAFT; echo \"oZPS0POrRieRtu\" | python yaft.py -i #enb_ip# -z ../#buildName# -R --ask_for_password"



cmds["scpWTS"] = "cd /opt/iphy/; scp -r ute@#baseip#:/opt/iphy/#iphyName# ."
cmds["updateiphy"] = "cd /opt/iphy/; rm -rf latest; ln -sf #iphyName# latest; cd latest;" \
                     "python fsmf_sw_update.py -i 192.168.200.#iphyID# --password oZPS0POrRieRtu --set_ge_ips 10.0.2.3#iphyID# 10.0.2.1 --set_log_ip 192.168.200.126 --set_fsm_id #iphyID# --set_srio_domain #iphyID# --save_iphy_xml"
cmds["killoldlua"] = "sudo pkill edaemon; sudo pkill egate"

username = "ute"
password = "ute"

def mutiThreadRun(serverlist, cmd):
    threads = []
    for i in range(len(serverlist)):
        t = threading.Thread(target=sshexecute, args=(serverlist[i], cmd),)
        threads.append(t)
    for i in range(len(serverlist)):
        threads[i].start()
    for i in range(len(serverlist)):
        threads[i].join()

def sshexecute(ip,cmdindex):
    try:
        cmd = cmds.get(cmdindex).replace("#baseip#", baseip).replace("#buildName#", servdict.get(ip).split(";")[1]).\
            replace("#enb_ip#", servdict.get(ip).split(";")[0]).replace("#iphyName#", iphyName)
        if cmdindex == "updateiphy":
            iphyID = str(iphyServList.index(ip) + 1)
            cmd = cmd.replace("#iphyID#", iphyID)
        # # #创建ssh客户端
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

        if "fsmf_sw_update.py" in cmd:
            if "End of the script, success" in outstring:
                print(ip + " *********  update iphy successful *********")
            else:
                print(ip + " *********  update iphy failed *********"
                           "failed details：" + outstring)


        if "yaft.py" in cmd:
            if "Flashing done" in outstring:
                print(ip + " *********  update enb successful *********")
            else:
                print(ip + " *********  update enb failed *********"
                           "failed details：" + outstring)

    except Exception, e:
        print e
    finally:
        client.close()


def updateEnb():
    # 检测zip包是否存在 不存在取拷贝
    # 检测解压后的文件是否存在， 不存在解压
    # yaft 升级

    allServList = []
    for key in servdict:
        allServList.append(key)

    # mutiThreadRun(allServList, "scpBuild")
    mutiThreadRun(allServList, "yaft")

def uploadIphy():
    mutiThreadRun(iphyServList, "scpWTS")
    mutiThreadRun(iphyServList, "updateiphy")
    sshexecute(baseip, "killoldlua")


if __name__ == "__main__":
    # uploadIphy()
    updateEnb()
