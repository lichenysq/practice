#-*-coding:utf-8-*-
import sys
import os
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='./getLatestEnbPackage.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level = logging.INFO,filemode='a',datefmt='%Y-%m-%d%I:%M:%S %p')

#包名
global targetPackageName
#执行时间，波兰时间，只具体到小时
global executTime
#执行间隔时间.单位：天
global intervalTime

targetPackageName = 'FL18SP_ENB'
executTime = 0

def getHtml(url):
    logging.info("getHtml  start....")
    logging.info("getHtml, the url is: " + url)
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.execute_script("return document.documentElement.outerHTML")
    except Exception, e:
         logging.info("getHtml  failed :" + e)

    logging.info("getHtml  end......")
    driver.close()

    return html

def downloadFLLatestPackage():
    dict = {}
    list = []

    url = "http://files.ute.inside.nsn.com/builds/enb/base/"

    html = getHtml(url)
    bs = BeautifulSoup(html)
    items = bs.find_all("a")
    for item in items:
        packname = item.string
        if packname.startswith(targetPackageName):
            temp = packname.split("_")
            if len(temp) > 4:
                version = int(temp[3])
                list.append(version)
                dict[version] = packname

    latestversion = max(list)
    latestPackageName = dict[latestversion]

    logging.info("get latest packagename :" + latestPackageName)



    driver = webdriver.Chrome()
    driver.get(url)
    aboutLink = driver.find_element_by_partial_link_text(latestPackageName)
    aboutLink.click()

    packagepagehtml = driver.execute_script("return document.documentElement.outerHTML")

    packagebs = BeautifulSoup(packagepagehtml)
    packageitems = packagebs.find_all("a")

    if len(packageitems) > 8:
        btssm = driver.find_element_by_xpath("/html/body/pre/a[3]")
        btssm.click()

        enb = driver.find_element_by_xpath("/html/body/pre/a[5]")
        enb.click()
    else:
        list.remove(latestversion)
        latestversion = max(list)
        latestPackageName = dict[latestversion]
        logging.info("relocat latest packagename :" + latestPackageName)

        driver = webdriver.Chrome()
        driver.get(url)
        aboutLink = driver.find_element_by_partial_link_text(latestPackageName)
        aboutLink.click()

        logging.info("start to download latest packagename :" + latestPackageName)

        btssm = driver.find_element_by_xpath("/html/body/pre/a[3]")
        btssm.click()

        enb = driver.find_element_by_xpath("/html/body/pre/a[5]")
        enb.click()

    time.sleep(3600)



def downloadTLLatestPackage():
    dict = {}
    list = []

    url = "http://files.ute.inside.nsn.com/builds/enb/base/"

    html = getHtml(url)
    bs = BeautifulSoup(html)
    items = bs.find_all("a")

    flname = targetPackageName
    flname = flname.replace('TL', 'FL', 1)

    for item in items:
        packname = item.string
        if packname.startswith(flname):
            temp = packname.split("_")
            if len(temp) > 4:
                version = int(temp[3])
                list.append(version)
                dict[version] = packname

    latestversion = max(list)
    latestPackageName = dict[latestversion]

    logging.info("get FDD latest packagename :" + latestPackageName)

    driver = webdriver.Chrome()
    driver.get(url)
    aboutLink = driver.find_element_by_partial_link_text(latestPackageName)
    aboutLink.click()

    packagepagehtml = driver.execute_script("return document.documentElement.outerHTML")

    packagebs = BeautifulSoup(packagepagehtml)
    packageitems = packagebs.find_all("a")

    latestTLPackageName = ""

    if len(packageitems) > 8:
        Manifest = driver.find_element_by_partial_link_text("Manifest.ini.txt")
        Manifest.click()
        Manifesthtml = driver.execute_script("return document.documentElement.outerHTML")
        Manifestbs = BeautifulSoup(Manifesthtml)
        Manifeststr = Manifestbs.find('pre').string
        latestTLPackageName = getcompatiblebuild(Manifeststr)

        logging.info("get TDD latest packagename :" + latestPackageName)

    else:
        list.remove(latestversion)
        latestversion = max(list)
        latestPackageName = dict[latestversion]
        logging.info("relocat FDD latest packagename :" + latestPackageName)

        driver = webdriver.Chrome()
        driver.get(url)
        aboutLink = driver.find_element_by_partial_link_text(latestPackageName)
        aboutLink.click()

        Manifest = driver.find_element_by_partial_link_text("Manifest.ini.txt")
        Manifest.click()
        Manifesthtml = driver.execute_script("return document.documentElement.outerHTML")
        driver.close()

        Manifestbs = BeautifulSoup(Manifesthtml)
        Manifeststr = Manifestbs.find('pre').string

        latestTLPackageName = getcompatiblebuild(Manifeststr)
        logging.info("get TDD latest packagename :" + latestPackageName)

    driver.close()

    driver = webdriver.Chrome()
    driver.get(url)
    aboutLink = driver.find_element_by_partial_link_text(latestTLPackageName)
    aboutLink.click()

    logging.info("start to download :" + latestPackageName)

    btssm = driver.find_element_by_xpath("/html/body/pre/a[3]")
    btssm.click()
    enb = driver.find_element_by_xpath("/html/body/pre/a[7]")
    enb.click()

    time.sleep(3600)



def getcompatiblebuild(text):
    buildName = ''
    text = str(text).replace(" ","")

    msgitems = text.split("\n")
    for msg in msgitems:
        msglist = msg.split("=")
        if cmp(msglist[0], "compatible_build_tdd_airscale") == 0:
            buildName = msglist[1]
            break
    print "get the compatible build:  " + buildName
    return buildName


def main():
    # executenow = sys.argv[1]
    executenow = "now"




    while True:
        now = datetime.datetime.now()
        if cmp(executenow, "now") == 0:
            break
        if now.hour == executTime:
            break
        # 半个小时检测一次
        time.sleep(1800)

    if targetPackageName.startswith("FL"):
        downloadFLLatestPackage()
    if targetPackageName.startswith("TL"):
        downloadTLLatestPackage()


if __name__ =="__main__":
    main()
