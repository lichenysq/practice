import csv

def checkMg3(filePath):
    msgIdIndex = None
    sfnIndex = None
    reCellIdIndex = None
    reEnbIdIndex = None
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
        elif item.startswith("relatedSCellCellId"):
            reCellIdIndex = i
        elif item.startswith("relatedSCellEnbId"):
            reEnbIdIndex = i

    judgeDict = {}

    for row in filedatalist:
        receiver = row[reCellIdIndex] + ":" + row[reEnbIdIndex]
        # newsfn16 = row[sfnIndex]
        newsfn = int(row[sfnIndex].replace("SFN=", ""), 16)

        if receiver in judgeDict:

            lastsfn = judgeDict[receiver][0]
            if newsfn - lastsfn > 0:
                if newsfn - lastsfn <= 4:
                    judgeDict[receiver] = [newsfn, row[0]]
                    continue
                else:
                    raise Exception("***** check message3 failed ****** \n"
                                    "please check:" + row[0] + " and " + judgeDict[receiver][1])
            elif newsfn + 1024 - lastsfn <= 4:
                judgeDict[receiver] = [newsfn, row[0]]
                continue
            else:
                raise Exception("***** check message3 failed ****** \n"
                                "please check:" + row[0] + " and " + judgeDict[receiver][1])

        else:
            judgeDict[receiver] = [newsfn, row[0]]

if __name__ == "__main__":
    # filePath = "C:\\N-5CG8250K26-Data\\shuyu\\Desktop\\enb1_emil.csv"
    # checkMg3(filePath)
    pass

