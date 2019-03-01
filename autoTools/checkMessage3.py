import csv

def checkMg3(filePath):
    msgIdIndex = None
    sfnIndex = None
    reCellIdIndex = None
    reEnbIdIndex = None
    incellIndex = None
    enbidIndex = None
    filedatalist = []

    with open(filePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            filedatalist.append(row)

    for i, item in enumerate(filedatalist[0]):

        if item.startswith("MSG_ID"):
            msgIdIndex = i
        elif item.startswith("SFN"):
            sfnIndex = i
        elif item.startswith("relatedSCellCellId") or item.startswith("relatedPCellCellId"):
            reCellIdIndex = i
        elif item.startswith("relatedSCellEnbId") or item.startswith("relatedPCellEnbId"):
            reEnbIdIndex = i
        elif item.startswith("lnCelId"):
            incellIndex = i
        elif item.startswith("enbId"):
            enbidIndex = i

    judgeDict = {}

    resultlist = []
    for row in filedatalist:

        if row[reCellIdIndex].startswith("relatedSCellCellId"):
            key1index = reCellIdIndex
            key2index = reEnbIdIndex
        else:
            key1index = incellIndex
            key2index = enbidIndex

        receiver = row[msgIdIndex] + ":" + row[key1index] + ":" + row[key2index]
        # newsfn16 = row[sfnIndex]
        newsfn = int(row[sfnIndex].replace("SFN=", ""), 16)

        if receiver in judgeDict:

            lastsfn = judgeDict[receiver][0]
            if newsfn - lastsfn > 0:
                if newsfn - lastsfn <= 4:
                    judgeDict[receiver] = [newsfn, row[0]]
                    continue
                else:
                    resultlist.append(row[0] + " and " + judgeDict[receiver][1])
                    continue
            elif newsfn + 1024 - lastsfn <= 4:
                judgeDict[receiver] = [newsfn, row[0]]
                continue
            else:
                resultlist.append(row[0] + " and " + judgeDict[receiver][1])
                continue
        else:
            judgeDict[receiver] = [newsfn, row[0]]

    if len(resultlist) > 0:
        raise Exception("***** check message3 failed ****** \n"
                        "please check:" + str(resultlist))

if __name__ == "__main__":
    # filePath = "C:\\N-5CG8250K26-Data\\shuyu\\Desktop\\enb1_emil.csv"
    # checkMg3(filePath)
    pass

