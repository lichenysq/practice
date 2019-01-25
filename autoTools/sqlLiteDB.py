#-*-coding:utf-8-*-
import sqlite3

def checkCaseIsExist(caseName, build, platform):
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CASE_RESULT WHERE CASE_NAME = (?) AND RELEASE = (?) AND PLATFORM = (?)',
                   (caseName, build, platform,))
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    if values == None or len(values) == 0:
        return False
    else:
        return True

def newcaseinfo(caseName, build, platform):

    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()

    cursor.execute('insert into CASE_RESULT (CASE_NAME, RELEASE, PLATFORM, FAIL, PASS) values (?, ?, ?, 0, 0)',
                   (caseName, build, platform))
    cursor.close()
    conn.commit()
    conn.close()

def addPass(caseName, build, platform):
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('update CASE_RESULT SET PASS = PASS + 1 WHERE CASE_NAME = (?) AND RELEASE = (?) AND PLATFORM = (?)',
                   (caseName, build, platform,))
    cursor.close()
    conn.commit()
    conn.close()

def addFailed(caseName, build, platform,):
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('update CASE_RESULT SET FAIL = FAIL + 1 WHERE CASE_NAME = (?) AND RELEASE = (?) AND PLATFORM = (?)',
                   (caseName, build, platform,))
    cursor.close()
    conn.commit()
    conn.close()


def createTable():
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE CASE_RESULT
           (CASE_NAME      VARCHAR(255),
           RELEASE         VARCHAR(255),
           PLATFORM        VARCHAR(255),
           FAIL            INT,
           PASS            INT,
           FAIL_RATE       INT,
           primary key (CASE_NAME,RELEASE,PLATFORM));''')
    cursor.close()
    conn.commit()
    conn.close()

# 小数点 四舍五入问题  待解决
def caculateRate():
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE CASE_RESULT SET FAIL_RATE = FAIL*100/(PASS+FAIL)')
    cursor.close()
    conn.commit()
    conn.close()

def collectAllInfo():
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()

    cursor.execute('SELECT CASE_NAME, PASS, FAIL, FAIL_RATE, RELEASE, PLATFORM FROM CASE_RESULT '
                   'ORDER BY FAIL_RATE DESC, FAIL DESC')
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values

def resetCount():
    conn = sqlite3.connect('CASE_RESULT.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE CASE_RESULT SET FAIL_RATE = 0, PASS = 0, FAIL = 0')
    cursor.close()
    conn.commit()
    conn.close()

# createTable()
# resetCount()

# if checkCaseIsExist("LTE1830_004_2CC_CA_20MHz_1UE_TM3_ULDL2_SSF7_Udp","TL00", "Airscale"):
#     print("exist")
#     # newcaseinfo("LTE1830_004_2CC_CA_20MHz_1UE_TM3_ULDL2_SSF7_Udp","TL00", "Airscale")
#
# addPass("LTE1830_004_2CC_CA_20MHz_1UE_TM3_ULDL2_SSF7_Udp","TL00", "Airscale")
# caculateRate()
# print(collectAllInfo())
