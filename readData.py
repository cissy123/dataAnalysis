import numpy as np
from collections import defaultdict
import chardet
import xlrd
def readTxtData(fileName,specialAlleleList):
    exampleList = defaultdict(list)
    alleleList = list()
    alleleData = list()
    newAlleleData = list()
    specialIndex = list()

    f = open(fileName, 'rb')#,encoding = 'UTF-16')
    d = f.read()
    if chardet.detect(d)['encoding'] == 'UTF-16':
        f = open(fileName,'r',encoding = 'UTF-16')
    elif chardet.detect(d)['encoding'] == 'ascii':
        f = open(fileName,'r')
    elif chardet.detect(d)['encoding'] == 'UTF-8-SIG':
        f = open(fileName,'r',encoding = 'UTF-8-SIG')

    lineNum = 0
    for line in f.readlines():
        line = line.strip()
        value_list = line.split('\t')
        if lineNum == 0:
            alleleList = value_list[2:]
        if not len(line) or lineNum == 0:
            lineNum += 1
            continue
        exampleList['exampleName'].append(value_list[0])
        exampleList['groupName'].append(value_list[1])

        alleleData.append(value_list[2:])
    # for  i in range(len(alleleData)):
    #     if len(alleleData[i]) != len(alleleList):
    #         print(i)
    #         print(alleleData[i])
            # print(exampleList['exampleName'][i])

    for i in specialAlleleList:
        if i in alleleList:
            ii = alleleList.index(i)
            specialIndex.append(ii)
            

    for i in range(len(exampleList['exampleName'])):
        for j in range(len(alleleList)):
            s = alleleData[i][j].split(',')
            if j in specialIndex:
                if len(s) == 2:
                    newAlleleData.append(s[0])
                    newAlleleData.append(s[-1])
                elif len(s) == 1:
                    newAlleleData.append(s[0])
                    newAlleleData.append(s[0])
            else:
                newAlleleData.append(s[0])
                
    if len(specialAlleleList) > 0:
        alleleList = updateList(alleleList, specialAlleleList)

    alleleNum = len(alleleList)
    data = np.array(newAlleleData).reshape(int(len(exampleList['exampleName'])), alleleNum)
    # print(data)
    return exampleList,alleleList,data

def readExcelData(fileName,specialAlleleList):
    exampleList = defaultdict(list)
    alleleList = list()
    alleleData = list()
    newAlleleData = list()
    specialIndex = list()

    ######open
    wb = xlrd.open_workbook(fileName)
    sh=wb.sheet_by_index(0)
    table = wb.sheets()[0] 
    #readData
    nrows = table.nrows
    ncols = table.ncols
    for i in range(1,nrows):
        alleleData.append(table.row_values(i)[2:])

    exampleList['exampleName'] = table.col_values(0)[1:]
    exampleList['groupName'] = table.col_values(1)[1:]

    alleleList = table.row_values(0)[2:]

    for i in specialAlleleList:
        if i in alleleList:
            ii = alleleList.index(i)
            specialIndex.append(ii)

    for i in range(len(exampleList['exampleName'])):
        for j in range(len(alleleList)):
            if type(alleleData[i][j]) == str:
                s = alleleData[i][j].split(',')
                # newAlleleData.append(float(s[0]))
                if j in specialIndex:
                    newAlleleData.append(float(s[0]))
                    newAlleleData.append(float(s[-1]))
                else:
                    newAlleleData.append(float(s[0]))
            elif j in specialIndex:
                newAlleleData.append(alleleData[i][j])
                newAlleleData.append(alleleData[i][j])
            else:
                newAlleleData.append(alleleData[i][j])
                
    if len(specialAlleleList) > 0:
        alleleList = updateList(alleleList, specialAlleleList)

    alleleNum = len(alleleList)
    data = np.array(newAlleleData).reshape(int(len(exampleList['exampleName'])), alleleNum)
    return exampleList,alleleList,data    

def updateList(oldList,name):
    indexList = list()
    for i in name:
        if i in oldList:
            indexList.append(oldList.index(i))

    counter = 0
    for x in indexList:
        oldList.insert(x+counter,name[counter])
        counter += 1
    return oldList
