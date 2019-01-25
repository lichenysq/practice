import matplotlib.pyplot as plt
import csv
import numpy as np
import os

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

def transListItemtoFloat(list):
    newlist = []
    for item in list:
        newlist.append(float(item))
    return newlist

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

def saveDictToFile(dict, filePath):
    filePath = filePath.replace(".csv", ".txt")
    with open(filePath, 'w') as f:
        for key in dict:
            f.write(key + "=" + str(dict[key]) + "\n")
        f.close()

def analyseCsv(filePath):
    #gap大小
    n = 6
    gaprange = 300
    tputcw1List = []
    tputcw2List = []
    fileArray = []
    ETtiTraceDlParUe_tbsCw1_index = None
    ETtiTraceDlParUe_tbsCw2_index = None
    ETtiTraceDlParUe_dataInDrb1_index = None
    ETtiTraceDlParUe_expectedThroughput_index = None
    EHarqParDl_harqReportSource_index = None
    EHarqParDl_ackNackDtxCw1_index = None
    EHarqParDl_ackNackDtxCw2_index = None
    gapIndexList = []
    x = []
    cw1 = []
    cw2 = []
    finalshowdata = {}


    with open(filePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        flag = 0
        for row in readCSV:
            # 找到起始行
            # ETtiTraceDlParUe_tbsCw1_index = None
            if "Time" in row:
                # 找到各个索引
                ETtiTraceDlParUe_tbsCw1_index = row.index("ETtiTraceDlParUe_tbsCw1")
                ETtiTraceDlParUe_tbsCw2_index = row.index("ETtiTraceDlParUe_tbsCw2")
                ETtiTraceDlParUe_dataInDrb1_index = row.index("ETtiTraceDlParUe_dataInDrb1")
                ETtiTraceDlParUe_expectedThroughput_index = row.index("ETtiTraceDlParUe_expectedThroughput")
                EHarqParDl_harqReportSource_index = row.index("EHarqParDl_harqReportSource")
                EHarqParDl_ackNackDtxCw1_index = row.index("EHarqParDl_ackNackDtxCw1")
                EHarqParDl_ackNackDtxCw2_index = row.index("EHarqParDl_ackNackDtxCw2")

                flag = 1
                continue

            if flag == 1:
                fileArray.append(row)
                tputcw1List.append(row[ETtiTraceDlParUe_tbsCw1_index])
                tputcw2List.append(row[ETtiTraceDlParUe_tbsCw2_index])

        # 找到gap  参考第一列， 找到连续n个为“—”的起始以及结束行
        for line in fileArray:
            i = fileArray.index(line)
            if fileArray[i][0] != "-":
                continue
            for j in range(n):
                if i + j < len(fileArray) and fileArray[i + j][0] == "-":
                    if j == n - 1:
                        # i 就是起始行
                        # 再继续找到结束行
                        while (fileArray[i + j][0] == "-"):
                            j = j + 1
                        tempgap = [i, i + j - 1]
                        if len(gapIndexList) == 0:
                            gapIndexList.append(tempgap)
                        elif i > gapIndexList[-1][1]:
                            gapIndexList.append(tempgap)

        # 展示包括gap前后300tti的数据  先整理出需要展示的的坐标
        finalshowindexlist = []
        finalshowdata["gapIndexList"] = gapIndexList

        for gap in gapIndexList:
            if gap[0] - gaprange > 0:
                a = gap[0] - 300
                if gapIndexList.index(gap) > 0 and a < gapIndexList[gapIndexList.index(gap) - 1][1]:
                    a = gapIndexList[gapIndexList.index(gap) - 1][1] + gaprange
            else:
                a = 0
                if gapIndexList.index(gap) > 0 and a < gapIndexList[gapIndexList.index(gap) - 1][1]:
                    a = gapIndexList[gapIndexList.index(gap) - 1][1] + gaprange

            if gap[1] + gaprange > len(fileArray):
                b = len(fileArray)
            else:
                b = gap[1] + gaprange

            finalshowindexlist.append([a, b])

        for j in range(len(finalshowindexlist)):
            i = 0
            for item in finalshowindexlist:
                if i > 0:
                    if abs(finalshowindexlist[i][0] - finalshowindexlist[i - 1][1]) < 100 or finalshowindexlist[i][0] < \
                            finalshowindexlist[i - 1][1]:
                        finalshowindexlist[i - 1][1] = finalshowindexlist[i][1]
                        finalshowindexlist.pop(i)
                i = i + 1

        # 展示全部数据
        finalshowindexlist = [[0, len(fileArray) - 1],]

        dataInDrb1List = []
        expected_t_put_list = []
        EHarqParDl_harqReportSource_list = []
        ackrateList = []
        ack_x = []

        for indexitem in finalshowindexlist:
            x = x + list(range(indexitem[0], indexitem[1]))

            gapfileArray = fileArray[indexitem[0]:indexitem[1]]

            # dataInDrb1
            dataInDrb1Listtemp = [x[ETtiTraceDlParUe_dataInDrb1_index] for x in gapfileArray]
            dataInDrb1Listtemp = transList(dataInDrb1Listtemp)
            dataInDrb1List = dataInDrb1List + dataInDrb1Listtemp

            # expected_t_put
            expected_t_put_listtemp = [x[ETtiTraceDlParUe_expectedThroughput_index] for x in gapfileArray]
            expected_t_put_listtemp = transList(expected_t_put_listtemp)
            expected_t_put_listtemp = [x / 1000 for x in expected_t_put_listtemp]
            expected_t_put_list = expected_t_put_list + expected_t_put_listtemp

            # EHarqParDl_harqReportSource    timeout
            EHarqParDl_harqReportSource_temp_list = [x[EHarqParDl_harqReportSource_index] for x in gapfileArray]
            po = 0
            EHarqParDl_harqReportSource_listtemp = []
            for item in EHarqParDl_harqReportSource_temp_list:
                if item == "timeout":
                    EHarqParDl_harqReportSource_listtemp.append(po)
                po = po + 1
            EHarqParDl_harqReportSource_list = EHarqParDl_harqReportSource_list + EHarqParDl_harqReportSource_listtemp

            # ack rate  per100tti
            EHarqParDl_ackNackDtxCw1_listtemp = [x[EHarqParDl_ackNackDtxCw1_index] for x in gapfileArray]
            EHarqParDl_ackNackDtxCw1_listtemp = splitList(EHarqParDl_ackNackDtxCw1_listtemp, 100)
            for ackitem in EHarqParDl_ackNackDtxCw1_listtemp:
                count = 0
                blank = 0
                for aitem in ackitem:
                    if aitem == "ACK":
                        count = count + 1
                    if aitem == "-":
                        blank = blank + 1
                if len(ackitem) - blank == 0:
                    rate = 0
                else:
                    rate = (count * 10000 / (len(ackitem) - blank))
                ackrateList.append(rate)

            ack_x = ack_x + list(range(int(indexitem[0]) + 50, int(indexitem[1] + 50), 100))

            # rank1
            templist = [x[EHarqParDl_ackNackDtxCw1_index] for x in gapfileArray]
            cw1temp = []
            i = 1
            for kw1item in templist:
                if kw1item == "-":
                    cw1temp.append(indexitem[0] + i)
                i = i + 1
            cw1 = cw1 + cw1temp

            # rank2
            templist = [x[EHarqParDl_ackNackDtxCw2_index] for x in gapfileArray]
            cw2temp = []
            i = 1
            for kw1item in templist:
                if kw1item == "-":
                    cw2temp.append(indexitem[0] + i)
                i = i + 1
            cw2 = cw2 + cw2temp

        finalshowdata["ack_rate_x"] = ack_x
        finalshowdata["ack_rate_y"] = ackrateList
        finalshowdata["cw1_x"] = cw1
        finalshowdata["cw1_y"] = [500] * len(cw1)
        finalshowdata["cw2_x"] = cw2
        finalshowdata["cw2_y"] = [-500] * len(cw2)
        finalshowdata["dataInDrb1List_x"] = x
        finalshowdata["dataInDrb1List_y"] = dataInDrb1List
        finalshowdata["expected_t_put_x"] = x
        finalshowdata["expected_t_put_y"] = expected_t_put_list
        finalshowdata["EHarqParDl_harqReportSource_x"] = EHarqParDl_harqReportSource_list
        finalshowdata["EHarqParDl_harqReportSource_y"] = [1000] * len(EHarqParDl_harqReportSource_list)


    # t_put
    tputcw1List = transList(tputcw1List)
    tputcw2List = transList(tputcw2List)

    tput_tti_List = np.array(tputcw1List) + np.array(tputcw2List)
    tput_sec_List = []
    for temp in splitList(tput_tti_List, 100):
        tput_sec_List.append(np.mean(temp))

    tput_x = list(range(0, len(tput_sec_List)))
    tput_x = [(x + 0.5) * 100 for x in tput_x]
    finalshowdata["tput_x"] = tput_x
    finalshowdata["tput_y"] = tput_sec_List

    # 设置x轴标签
    timelist = [x[0] for x in fileArray]
    timelist = splitList(timelist, 10)
    xlable = [x[0] for x in timelist]
    xlableindex = list(range(0, 10 * len(xlable) + 1, 10))

    finalshowdata["xlable"] = xlable
    finalshowdata["xlableindex"] = xlableindex
    # plt.xticks(xlableindex, xlable, rotation=45)

    saveDictToFile(finalshowdata, filePath)

def readAndShow(filepath):
    readoutdataDict = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()

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
            i = i.replace("[", "")
            i = i.replace("]", "")
            i = i.split("=")
            if i[0] != "xlable" and i[0] != "gapIndexList":
                if len(i) > 1 and len(i[1]) > 1 and i[1].replace(",", "").replace(".", "").replace("-","").isdigit():
                    readoutdataDict[i[0]] = transListItemtoFloat(i[1].split(","))
            elif i[0] == "xlable":
                readoutdataDict[i[0]] = i[1].split(",")
            elif i[0] == "gapIndexList":
                if len(i) > 1 and len(i[1]) > 1:
                    readoutdataDict[i[0]] = splitList(i[1].split(","), 2)




        plt.plot(readoutdataDict["dataInDrb1List_x"], readoutdataDict["dataInDrb1List_y"], label='dataInDrb1', marker='.')
        plt.plot(readoutdataDict["expected_t_put_x"], readoutdataDict["expected_t_put_y"], label='expected t_put', marker='.')
        if "EHarqParDl_harqReportSource_x" in  readoutdataDict:
             plt.bar(readoutdataDict["EHarqParDl_harqReportSource_x"], readoutdataDict["EHarqParDl_harqReportSource_y"], label='timeout',fc="r", alpha=0.8)

        plt.plot(readoutdataDict["ack_rate_x"], readoutdataDict["ack_rate_y"], label='ack rate', marker='.')
        plt.bar(readoutdataDict["cw1_x"], readoutdataDict["cw1_y"], label='miss cw1', fc="orange", alpha=0.8)
        plt.bar(readoutdataDict["cw2_x"], readoutdataDict["cw2_y"], label='miss cw2', fc="k", alpha=0.8)
        plt.plot(readoutdataDict["tput_x"], readoutdataDict["tput_y"], label='t_put(/1000)', marker='o')
        plt.xticks(readoutdataDict["xlableindex"], readoutdataDict["xlable"], rotation=45)

        # print(gapIndexList)
        # gap区域 设置背景色示意
        if "gapIndexList" in readoutdataDict:
            for item in readoutdataDict["gapIndexList"]:
                temp_x = readoutdataDict["dataInDrb1List_x"][int(item[0]):int(item[1]) + 1]
                y1 = [0] * len(temp_x)
                y2 = [50000] * len(temp_x)
                plt.fill_between(temp_x, y1, y2, where=(y1 < y2), facecolor='k', alpha=0.35)

        plt.xlabel('tti')
        plt.ylabel('value')
        plt.title('ttiTrace')
        plt.grid(color='k', linestyle='--', linewidth=1,alpha=0.3)
        plt.title(filepath)
        plt.legend()
        plt.show()

if __name__ =="__main__":

    filename = ""
    path = os.getcwd()
    for item in os.listdir(path):
        if item.startswith("tti") and item.endswith(".csv"):
            filename = item
    filepath = "./" + filename

    # analyseCsv(filepath)
    readAndShow(filepath.replace(".csv", ".txt"))









































