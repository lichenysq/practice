#-*-coding:utf-8-*-
import datetime
import time
from selenium import webdriver
import os

def clickextend(envid, username, password):
    driver = webdriver.Chrome()
    url = "https://cloud.ute.nsn-rdnet.net/reservation/" + str(envid) + "/show"
    driver.get(url)
    usernameinput = driver.find_element_by_xpath("//*[@id=\"id_username\"]")
    usernameinput.send_keys(username)

    passwordinput = driver.find_element_by_xpath("//*[@id=\"id_password\"]")
    passwordinput.send_keys(password)

    login = driver.find_element_by_xpath("//*[@id=\"id_login_btn\"]")
    login.click()

    extend = driver.find_element_by_xpath("//*[@id=\"extend-button\"]")
    extend.click()
    driver.quit()




envid = input('please enter your env ID: ')

# 30分钟执行一次
while True:
    username = ""
    password = ""

    fileflag = os.path.exists("config")
    if fileflag == False:
        username = input('please enter your username: ')
        password = input('please enter your password: ')
        with open("./config", 'w') as f:
            f.write("username=" + username + "\n")
            f.write("password=" + password)
            f.close()

    with open("./config", 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            username = input('please enter your username: ')
            password = input('please enter your password: ')
            with open("./config", 'w') as f:
                f.write("username=" + username + "\n")
                f.write("password=" + password)
                f.close()
        else:
            for i in lines:
                # 忽略注释
                if i[0] == "#":
                    continue
                if i == '\n':
                    continue
                # 去空格
                i = i.replace(" ", "")
                # 去回车
                i = i.replace("\n", "")
                i = i.replace("'", "")
                i = i.split("=")
                if i[0] == "username":
                    username = i[1]
                elif i[0] == "password":
                    password = i[1]

    envidlist = envid.split(",")
    for item in envidlist:
      clickextend(item, username, password)
    print(" ")
    print("this programe will click extend button every 30mins, please don't close this window")
    print("waiting ...")
    time.sleep(1800)
    now = datetime.datetime.now()
    print(now)
    print("start to click extend button")
    for item in envidlist:
      clickextend(item, username, password)



