import chardet
import numpy as np
from collections import defaultdict
# import pandas as pd
from pandas import DataFrame
import xlrd
import os
import re

from memory_profiler import profile
import profiler
# from collections import defaultdict
# import numpy as np

# fileName = 'Mayans.txt'
# f = open(fileName, 'rb')#,encoding = 'UTF-16')
# d = f.read()
# print(chardet.detect(d)['encoding'])

# if chardet.detect(d)['encoding'] == 'UTF-16':
#     f = open(fileName,'r',encoding = 'UTF-16')
#     print('a')
# elif chardet.detect(d)['encoding'] == 'ascii':
#     f = open(fileName,'r')
#     print('b')
# elif chardet.detect(d)['encoding'] == 'UTF-8-SIG':
#     f = open(fileName,'r',encoding = 'UTF-8-SIG')
#     print('c')
# for line in f.readlines():
# 	print(line)



def readData(fileName,specialAlleleList):
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
    print(len(alleleList))  

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
                    # newAlleleData.append(float(s[0]))
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


# def readData(fileName,specialAlleleList):
#     exampleList = defaultdict(list)
#     alleleList = list()
#     alleleData = list()
#     newAlleleData = list()
#     specialIndex = list()

#     f = open(fileName, 'rb')#,encoding = 'UTF-16')
#     d = f.read()
#     if chardet.detect(d)['encoding'] == 'UTF-16':
#         f = open(fileName,'r',encoding = 'UTF-16')
#     elif chardet.detect(d)['encoding'] == 'ascii':
#         f = open(fileName,'r')
#     elif chardet.detect(d)['encoding'] == 'UTF-8-SIG':
#         f = open(fileName,'r',encoding = 'UTF-8-SIG')

#     lineNum = 0
#     for line in f.readlines():
#         line = line.strip()
#         value_list = line.split('\t')
#         if lineNum == 0:
#             alleleList = value_list[2:]
#         if not len(line) or lineNum == 0:
#             lineNum += 1
#             continue
#         exampleList['exampleName'].append(value_list[0])
#         exampleList['groupName'].append(value_list[1])

#         alleleData.append(value_list[2:])
#     # for  i in range(len(alleleData)):
#     #     if len(alleleData[i]) != len(alleleList):
#     #         print(i)
#     #         print(alleleData[i])
#             # print(exampleList['exampleName'][i])

#     for i in specialAlleleList:
#         if i in alleleList:
#             ii = alleleList.index(i)
#             specialIndex.append(ii)
            

#     for i in range(len(exampleList['exampleName'])):
#         for j in range(len(alleleList)):
#             s = alleleData[i][j].split(',')
#             if j in specialIndex:
#                 if len(s) == 2:
#                     newAlleleData.append(s[0])
#                     newAlleleData.append(s[-1])
#                 elif len(s) == 1:
#                     newAlleleData.append(s[0])
#                     newAlleleData.append(s[0])
#             else:
#                 newAlleleData.append(s[0])
                
#     if len(specialAlleleList) > 0:
#         alleleList = updateList(alleleList, specialAlleleList)

#     alleleNum = len(alleleList)
#     data = np.array(newAlleleData).reshape(int(len(exampleList['exampleName'])), alleleNum)
#     # print(data)
#     return exampleList,alleleList,data

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
def grouping(exampleList, alleleData):
    group = defaultdict(list)
    group['groupName'] = exampleList['groupName']
    for i in range(len(exampleList['exampleName'])):
        group['exampleName'].append(exampleList['exampleName'][i])
        # group['alleleData'].append(alleleData[i])

    df = DataFrame(group)
    groupedData = df.groupby(df['groupName'])
    return groupedData

# @profile
def matchDiff(alleleData,groupedData, group):
    # matchmode = 0
    # seletedGroupindex = defaultdict(list)
    # result = defaultdict(list)
    # # print(groupedData.get_group(x))
    # index = groupedData.indices
    # for x in group['AllSelect']:
    #     seletedGroupindex['groupName'].append(x)
    #     seletedGroupindex['dataIndex'].append(index[x])
        
    #     print(index[x])

    # for i in range(len(seletedGroupindex['dataIndex'])):
    #     for j in range(i+1,len(seletedGroupindex['dataIndex'])):
    #         print(seletedGroupindex['groupName'][i] +' ' + seletedGroupindex['groupName'][j])
    #         for k in range(len(seletedGroupindex['dataIndex'][i])):
    #             for l in range(len(seletedGroupindex['dataIndex'][j])):
    #                 data1Index = seletedGroupindex['dataIndex'][i][k]
    #                 data2Index = seletedGroupindex['dataIndex'][j][l]
                




#########################################################3
            #         print(seletedGroupindex['dataIndex'][i][k])
            # print(seletedGroupindex['dataIndex'][i][j])
    def matchDiff(data, group):
        matchMode = 0
        if len(group['AllSelect']) < 2:
            QMessageBox.information(self,"warning","please select more than 1 group", QMessageBox.Yes | QMessageBox.No)
            return
        seletedGroupData = defaultdict(list)
        result = defaultdict(list)
        for i in data:
            name = i[0]
            if i[0] in group['AllSelect']:
                seletedGroupData['groupName'].append(name)
                seletedGroupData['alleleData'].append(i[1]['alleleData'])
                seletedGroupData['exampleName'].append(i[1]['exampleName'])

        for num1 in range(len(seletedGroupData['alleleData'])):
            for num2 in range(num1 + 1, len(seletedGroupData['alleleData'])):
                groupAdata = list(seletedGroupData['alleleData'][num1])
                groupBdata = list(seletedGroupData['alleleData'][num2])
                exampleA = list(seletedGroupData['exampleName'][num1])
                exampleB = list(seletedGroupData['exampleName'][num2])
                groupNameA = seletedGroupData['groupName'][num1]
                groupNameB = seletedGroupData['groupName'][num2]
                # for i in groupAdata:
                #     for j in groupBdata:
                for n1 in range(len(groupAdata)):
                    for n2 in range(len(groupBdata)):
                        exampleNameA = exampleA[n1]
                        exampleNameB = exampleB[n2]
                        resultString = list()
                        # v1 = list()
                        # v2 = list()
                        # for i in groupAdata[n1]:
                        #     if '.' in i:
                        #         v1.append(float(i))
                        #     else:
                        #         v1.append(int(i))
                        # for i in groupBdata[n2]:
                        #     if '.' in i:
                        #         v2.append(float(i))
                        #     else:
                        #         v2.append(int(i))
                        v1 = list(i for i in groupAdata[n1])
                        v2 = list(i for i in groupBdata[n2])
                        v = list(map(lambda x: x[0] - x[1], zip(v2, v1)))
                        currentmisMatchSteps = round(sum(abs(i) for i in v),3)
                        currentmisMatchNum = len(v) - v.count(0)
                        if matchMode == 1:  # 1:matchmode. default 0:mismatchmode
                            currentmisMatchSteps = 0
                            currentmisMatchNum = v.count(0)
                        result['groupName'].append('(' + groupNameA + ',' + groupNameB + ')')
                        result['examplePair'].append('(' + exampleNameA + ',' + exampleNameB + ')')
                        result['misMatchNum'].append(currentmisMatchNum)
                        result['misMatchSteps'].append(currentmisMatchSteps)
                        if currentmisMatchNum == 0:
                            result['misMatchRatio'].append(0)
                        else:
                            result['misMatchRatio'].append(round(float(currentmisMatchSteps / currentmisMatchNum),3))
                        for n in range(len(v)):
                            resultString.append(str(round(abs(v[n]),3)) + '(' + str(v1[n]) + ',' + str(v2[n]) + ')')

                        result['misMatchDetail'].append(resultString)




if __name__ == '__main__':
    # typeFile = os.path.splitext('E:\Projects\dataAnalysis_py\Mayans1.xlsx')[-1]
    # print(typeFile in ['.xlsx','.xls'])
    # exampleList,alleleList,alleleData = readData('E:\Projects\dataAnalysis_py\Mayans1.xlsx',['DYS456','DYS389I'])
    # print(alleleData[0])
    # groupedData = grouping(exampleList, alleleData)
    # selectedGroupDiff = defaultdict(list)
    # # selectedGroupDiff['AllSelect'] = ['O1a1a1b2', 'O1a1a2', 'O1b1a1a1a', 'O1b1a1a1a1a', 'O1b1a1a1a1a1', 'O1b1a1a1a1a2', 'O1b1a1a1a1b', 'O1b1a1a1a1b1', 'O1b1a1a1b', 'O1b1a2a', 'O1b1a2b', 'O1b2', 'O2', 'O2a1', 'O2a1c', 'O2a1c1a1a1a', 'O2a1c1a1a1a1a1a1', 'O2a1c1a1a1a1a1a1a1a', 'O2a1c1a1a1a1a1a1a2', 'O2a1c1a1a1a1a1a1b', 'O2a1c1a1a1a1a1a1b\xa0\xa0', 'O2a2a1', 'O2a2a1a1a', 'O2a2b', 'O2a2b1a1', 'O2a2b1a1a', 'O2a2b1a1a1', 'O2a2b1a1a3', 'O2a2b1a1a4', 'O2a2b1a1a6', 'O2a2b1a2', 'O2a2b1a2a1', 'O2a2b1a2a1a3', 'O2a2b1a2a1a3b1', 'O2a2b1a2a1a3b2b2', 'Q1a2']
    # selectedGroupDiff['AllSelect'] = ['O1a1a1b2', 'O1a1a2', 'O1b1a1a1a']
    # if len(selectedGroupDiff['AllSelect']) > 0:
    #         matchDiff(alleleData,groupedData, selectedGroupDiff)


    # wb = xlrd.open_workbook('Mayans1.xlsx')
    # sh=wb.sheet_by_index(0)
    # table = wb.sheets()[0]  
    # # cellA1 = sh.cell(0,0) 


    # exampleList = defaultdict(list)
    # alleleList = list()
    # alleleData = list()
    # newAlleleData = list()
    # specialIndex = list()

    # nrows = table.nrows
    # ncols = table.ncols
    # for i in range(1,nrows):
    #     alleleData.append(table.row_values(i)[2:])
    # # print(alleleData)
    # #     for j in range(ncols):
    # #         pass
    # exampleList['exampleName'] = table.col_values(0)[2:]
    # exampleList['groupName'] = table.col_values(1)[2:]

    # alleleList = table.row_values(0)[2:]
    # print
    # # print(table.cell(1,2).ctype )
    # print(type(alleleData[0][0])== str)
    figname = '40_Q*'
    specialCharacter = ['*','/']
    for x in specialCharacter:
        if x in figname:
            figname = figname.replace(x, '9')
            print(x)
    print(figname)