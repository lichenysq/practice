#-*-coding:utf-8-*-

import matplotlib.pyplot as plt
import csv
import numpy as np

def splitList(list,step):
    newlist = []
    index = 0
    while(index < len(list) - step):
        if index + step > len(list):
            rightIndex = len(list) - 1
        else:
            rightIndex = index + step
        newlist.append(list[index:rightIndex])
        index = index + step

    if (index > len(list) - step):
        newlist.append(list[index:])

    return newlist

def transList(list):
    newList = []
    for item in list:
        if item == "-":
            if len(newList) == 0:
                item = 0
            else:
                item = newList[-1]
        newList.append(int(item))
    return newList

def getColumnNameList(filePath):
    with open(filePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if "Time" in row:
                return row

def getFileArray(filePath):
    with open(filePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        flag = 0
        fileArray = []
        for row in readCSV:
            # 找到起始行
            if "Time" in row:
                flag = 1
                continue
            if flag == 1:
                fileArray.append(row)
        return fileArray

def dealSingleColumn(columnNmae, type, size, trans, value):
    columnIndex = columnNameList.index(columnNmae)

    if type == "plot":
        columnData = [x[columnIndex] for x in fileArray]
        columnData = transList(columnData)
        if trans.startswith("*"):
            trans = int(trans.replace("*", ""))
            columnData = [x * trans for x in columnData]
        elif trans.startswith(""):
            trans = int(trans.replace("/", ""))
            columnData = [x / trans for x in columnData]

        ave_y = []
        for temp in splitList(columnData, size):
            ave_y.append(np.mean(temp))
        ave_x = list(range(0, len(ave_y)))
        ave_x = [(x + 0.5) * size for x in ave_x]

        if len(ave_x) != len(ave_y):
            print("11111111111")
        add2plt(ave_x, ave_y, columnNmae, type)

    elif type == "plot_percent":
        columnData = [x[columnIndex] for x in fileArray]
        rateList = []
        # 百分比
        columnData = splitList(columnData, 100)
        for item in columnData:
            count = 0
            blank = 0
            for temp in item:
                if temp == "-":
                    blank = blank + 1

                if trans.startswith("="):
                    trans = trans.replace("=", "")
                    if temp == trans:
                        count = count + 1
                elif trans.startswith("!="):
                    trans = trans.replace("!=", "")
                    if temp != trans:
                        count = count + 1

            if len(item) - blank == 0:
                rate = 0
            else:
                rate = (count * 100 / (len(item) - blank))
            rateList.append(rate)

        rate_x = list(range(50,lineNum + 50, 100))
        if len(rate_x) != len(rateList):
            print("2222222")

        add2plt(rate_x, rateList, columnNmae, type)

    elif type == "bar":
        columnData = [x[columnIndex] for x in fileArray]
        mark_x = []
        i = 1
        for temp in columnData:
            if trans.startswith("="):
                trans = trans.replace("=", "")
                if temp == trans:
                    mark_x.append(i)
            elif trans.startswith("!="):
                trans = trans.replace("!=", "")
                if temp != trans:
                    mark_x.append(i)

            i = i + 1
            mark_y = [int(value)] * len(mark_x)

            add2plt(mark_x, mark_y, columnNmae, type)

def add2plt(x, y, columnNmae, type):
    if type.startswith("plot"):
        plt.plot(x, y, label=columnNmae)
    elif type.startswith("bar"):
        plt.bar(x, y, label=columnNmae)



filepath = "./ttiTraceTest.csv"
fileArray = getFileArray(filepath)
lineNum = len(fileArray)
columnNameList = getColumnNameList(filepath)

dealSingleColumn("ETtiTraceDlParUe_tbsCw1", "plot", 1, "/256", "")


plt.title('ttiTrace')
plt.grid(color='k', linestyle='--', linewidth=1, alpha=0.3)
plt.title(filepath)
plt.legend()
plt.show()

