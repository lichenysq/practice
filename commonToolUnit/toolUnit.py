#-*-coding:utf-8-*-
import sys
import urllib
import os
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='../../LOG/FailedCaseAutoRerun.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level = logging.DEBUG,filemode='a',datefmt='%Y-%m-%d%I:%M:%S %p')


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




# caseDetailHtml = getHtml("https://4g-rep-portal.wroclaw.nsn-rdnet.net/qc/instance/details/1182770/?fs=4g")
# # 收录casename 和 path
# caseDetailBs = BeautifulSoup(caseDetailHtml)
# tds = caseDetailBs.find_all("td")
# name = tds[3]
# print name

