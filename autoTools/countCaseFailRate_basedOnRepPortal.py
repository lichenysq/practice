#-*-coding:utf-8-*-
import sys
import datetime
import time
import sqlLiteDB
from selenium import webdriver
import xlwt
import datetime


def generateExcel():
    sqlLiteDB.caculateRate()
    finalresult = sqlLiteDB.collectAllInfo()
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 0, "CASE_NAME")
    sheet.write(0, 1, "PASS_TIMES")
    sheet.write(0, 2, "FAIL_TIMES")
    sheet.write(0, 3, "FAIL_RATE %")
    sheet.write(0, 4, "RELEASE")
    sheet.write(0, 5, "PLAT_FORM")

    i = 1
    for case in finalresult:
        sheet.write(i,0,case[0])
        sheet.write(i,1,case[1])
        sheet.write(i,2,case[2])
        sheet.write(i,3,str(case[3]) + "%")
        sheet.write(i,4,case[4])
        sheet.write(i,5,case[5])
        i = i+1
    filename = "CRT_CASE_FAIL_RATE_" + datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S") + ".xls"
    wbk.save(filename)

def main(url):
    page = 0
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_xpath("//*[@id=\"id_username\"]").send_keys("shuyu")
    driver.find_element_by_xpath("//*[@id=\"id_password\"]").send_keys("1QAZ2wsx")
    driver.find_element_by_xpath("//*[@id=\"submit-id-sign_in\"]").click()

    # 等待页面加载完成
    time.sleep(15)
    pageElement = driver.find_element_by_xpath("//*[@id=\"rep-main\"]/div/div/div[3]/div[2]/div[1]/div[1]/span")
    page = int(pageElement.text.replace("/", ""))

    for i in range(0, page):
        temp = driver.find_elements_by_class_name("ui-grid-canvas")
        dataparaent = temp[-1]
        datalist = dataparaent.find_elements_by_css_selector("div[class=\"ui-grid-row ng-scope\"]")

        print(len(datalist))
        for item in datalist:
            result = item.find_element_by_css_selector("div[class=\"ui-grid-cell ng-scope ui-grid-coluiGrid-0008\"]").\
                find_element_by_tag_name("div").text
            result = result.replace(" ", "")
            # print(result)
            if result == "environmentissue":
                continue

            caseName = item.find_element_by_css_selector("a[class=\"a ng-binding\"]").text.replace(" ","")
            # print(caseName)

            info = item.find_elements_by_css_selector("div[class=\"ui-grid-cell-contents ng-binding ng-scope\"]")
            build = info[0].text.split("_")[0]
            if build.startswith("SBTS") and info[0].text.split("_")[1].startswith("TDD"):
                build = build + info[0].text.split("_")[1]

            platform = info[1].text
            # print(build)
            # print(platform)
            if not sqlLiteDB.checkCaseIsExist(caseName, build, platform):
                sqlLiteDB.newcaseinfo(caseName, build, platform)
            if result == "passed":
                sqlLiteDB.addPass(caseName, build, platform)
                # print(caseName+build+platform+ "pass")
                # print(sqlLiteDB.collectAllInfo())

            else:
                sqlLiteDB.addFailed(caseName, build, platform)
                # print(sqlLiteDB.collectAllInfo())

        if i == page:
            continue
        driver.find_element_by_xpath("//*[@id=\"rep-main\"]/div/div/div[3]/div[2]/div[1]/div[1]/button[3]").click()
        time.sleep(15)


begindate = "2018-12-11"
enddate = "2019-01-08"
url = "https://4g-rep-portal.wroclaw.nsn-rdnet.net/reports/test-runs/?end_ft=#beginDate#%2000:00:00,#endDate#%2023:59:59&" \
      "columns=test_case.name,result,build,test_case.test_instance.platform,test_case.test_instance.organization&org=4G_ASL2_HZH%20-%20SG%205&limit=200"
url = url.replace("#beginDate#", begindate)
url = url.replace("#endDate#", enddate)

print(datetime.datetime.now())

sqlLiteDB.resetCount()
print(url)
main(url)
sqlLiteDB.caculateRate()
generateExcel()
print(datetime.datetime.now())



