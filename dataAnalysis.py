# -*- coding: utf-8 -*-
import numpy as np
import re
import sys
import os

from collections import defaultdict
from pandas import DataFrame

from PyQt5.QtWidgets import QMainWindow, QFileDialog,QTableWidgetItem,QTableWidget,QMessageBox
from ui_dataanalysis import Ui_dataAnalysis

import readData
import groupWidget
import histogram

class dataAnalysis(QMainWindow):
    """mainWindow"""
    groupedData = dict()
    alleleList = list()
    matchMode = 0
    exampleList = defaultdict(list)
    resultDiff = defaultdict(list)
    resultSame = defaultdict(list)
    file = ''
    

    def __init__(self, parent=None):
        super(dataAnalysis, self).__init__(parent)
        # loadUi('dataanalysis.ui', self)
        self.ui=Ui_dataAnalysis()  
        self.ui.setupUi(self)
        self.ui.pb_data.clicked.connect(self.sl_getDataFile)

        #open groupSelect window
        self.ui.pb_groupSelect.clicked.connect(self.sl_groupSelect)

        self.ui.rb_mismatch.setChecked(True)
        self.ui.rb_mismatch.toggled.connect(self.checkMismatchMode)
        self.ui.rb_match.setChecked(True)
        self.ui.rb_match.toggled.connect(self.checkMatchMode)

        self.ui.pb_save.clicked.connect(self.save)


    def sl_getDataFile(self):
        text = self.ui.te_specialAllele.toPlainText()

        global alleleList,file,exampleList
        alleleList = []
        file = []
        exampleList = []
        file,_= QFileDialog.getOpenFileName(self, "open example file", "",
                                               "Excel File (*.xlsx);;Excel File (*.xls);;Text File(*.txt)")
        if len(file) == 0:
            return
        self.ui.le_data.setText(file)
        #check specialAllele isempty
        if len(text)>0:
            specialAlleleList = re.split('[ ,.\n\t]', text)
        else:
            specialAlleleList = []
        # specialAlleleList = []

        #check type of file 
        typeFile = os.path.splitext(file)[-1]
        if typeFile in ['.xlsx','.xls']:
            exampleList,alleleList,alleleData =readData.readExcelData(file,specialAlleleList)

        else:
            exampleList,alleleList,alleleData = readData.readTxtData(file,specialAlleleList)

        self.grouping(exampleList, alleleData)

    def sl_groupSelect(self):
        self.ui.pb_groupSelect.setEnabled(False)
        global exampleList
        # exampleList = readData.readExempleFile('example.txt')
        g = groupWidget.groupWidget()
        g.setWindowTitle('groupSelect')
        g.buildTree(np.unique(exampleList['groupName']))
        g.show()
        g.exec_()

        self.ui.pb_groupSelect.setEnabled(True)

        # refresh groupSelectList
        global groupedData
        # for x in groupedData:
        #     print(x)
        # print(groupedData)
        selectedGroupSame = g.treeItemChangedSame()
        if len(selectedGroupSame['AllSelect']) > 0:
            self.matchSame(groupedData, selectedGroupSame)

        selectedGroupDiff = g.treeItemChangedDiff()
        if len(selectedGroupDiff['AllSelect']) > 0:
            self.matchDiff(groupedData, selectedGroupDiff)

    def grouping(self, exampleList, alleleData):
        group = defaultdict(list)
        group['groupName'] = exampleList['groupName']
        for i in range(len(exampleList['exampleName'])):
            group['exampleName'].append(exampleList['exampleName'][i])
            group['alleleData'].append(alleleData[i])

        df = DataFrame(group)
        global groupedData
        groupedData = []
        groupedData = df.groupby(df['groupName'])


    def matchSame(self, data, group):
        global  matchMode,resultSame
        resultSame = []
        result = defaultdict(list)

        for i in group['AllSelect']:
            for j in data:
                if j[0] == i:
                    length = len(j[1])
                    if length > 1:
                        newCurrentAllele = list()
                        newExampleName = list()
                        CurrentAllele = j[1]['alleleData']
                        ExampleName = j[1]['exampleName']
                        for a1 in CurrentAllele:
                            newCurrentAllele.append(a1)
                        for a2 in ExampleName:
                            newExampleName.append(a2)


                        for n1 in range(length):
                            for n2 in range(n1 + 1, length):
                                resultString = list()
                                v1 = list(float(i) for i in newCurrentAllele[n1])
                                v2 = list(float(i) for i in newCurrentAllele[n2])
                                v = list(map(lambda x: x[0] - x[1], zip(v2, v1)))
                                currentmisMatchSteps = round(sum(abs(i) for i in v),3)
                                currentmisMatchNum = len(v) - v.count(0)
                                if matchMode == 1:#matchmode. default mismatchmode
                                    currentmisMatchSteps = 0
                                    currentmisMatchNum  = v.count(0)
                                result['groupName'].append(i)
                                result['examplePair'].append('(' + newExampleName[n1] + ',' + newExampleName[n2] + ')')
                                result['misMatchNum'].append(currentmisMatchNum)
                                result['misMatchSteps'].append(currentmisMatchSteps)
                                if currentmisMatchNum == 0:
                                    result['misMatchRatio'].append(0)
                                else:
                                    result['misMatchRatio'].append(round(float(currentmisMatchSteps / currentmisMatchNum),3))
                                for n in range(len(v)):
                                    resultString.append(str(round(abs(v[n]),3)) + '(' + str(v1[n]) + ',' + str(v2[n]) + ')')
                                result['misMatchDetail'].append(resultString)
        resultSame = result

        if len(resultSame['groupName']) >0:
            self.showTableSame(resultSame,matchMode)
            self.showHistogram(resultSame,'same')

    def matchDiff(self, data, group):
        global  matchMode
        if len(group['AllSelect']) < 2:
            QMessageBox.information(self,"warning","please select more than 1 group", QMessageBox.Yes | QMessageBox.No)
            return
        seletedGroupData = defaultdict(list)
        global resultDiff
        resultDiff = []
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
                        v1 = list(float(i) for i in groupAdata[n1])
                        v2 = list(float(i)  for i in groupBdata[n2])
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
        resultDiff = result
        if len(resultDiff['groupName']) >0:
            self.showTableDiff(resultDiff,matchMode)
            self.showHistogram(resultDiff,'diff')

    def showTableSame(self, result,matchMode):
        # self.ui.tw_same
        global alleleList
        alleleNum = len(alleleList)
        self.ui.tw_same.setColumnCount(5)
        self.ui.tw_same.setRowCount(len(result['groupName']) + 1)
        # self.ui.tw_same.setRowCount(5)

        self.ui.tw_same.setItem(0, 0, QTableWidgetItem("groupName"))
        self.ui.tw_same.setItem(0, 1, QTableWidgetItem("examplePair"))
        if matchMode == 0:
            self.ui.tw_same.setItem(0, 2, QTableWidgetItem("misMatchNum"))
            self.ui.tw_same.setItem(0, 3, QTableWidgetItem("misMatchSteps"))
            self.ui.tw_same.setItem(0, 4, QTableWidgetItem("misMatchRatio"))
        else:
            self.ui.tw_same.setItem(0, 2, QTableWidgetItem("matchNum"))
            self.ui.tw_same.setItem(0, 3, QTableWidgetItem("matchSteps"))
            self.ui.tw_same.setItem(0, 4, QTableWidgetItem("matchRatio"))
        self.ui.tw_same.setEditTriggers(QTableWidget.NoEditTriggers)

        # for n in range(len(alleleList)):
        #     self.ui.tw_same.setItem(0, n + 5, QTableWidgetItem(alleleList[n]))
        #
        for i in range(self.ui.tw_same.rowCount() - 1):
            self.ui.tw_same.setItem(i + 1, 0, QTableWidgetItem(result['groupName'][i]))
            self.ui.tw_same.setItem(i + 1, 1, QTableWidgetItem(result['examplePair'][i]))
            self.ui.tw_same.setItem(i + 1, 2, QTableWidgetItem(str(result['misMatchNum'][i])))
            self.ui.tw_same.setItem(i + 1, 3, QTableWidgetItem(str(result['misMatchSteps'][i])))
            self.ui.tw_same.setItem(i + 1, 4, QTableWidgetItem(str(round(result['misMatchRatio'][i], 3))))
            # for j in range(alleleNum):
            #     self.ui.tw_same.setItem(i + 1, j + 5, QTableWidgetItem(result['misMatchDetail'][i][j]))

    def showTableDiff(self, result,matchMode):
        # print(result['groupName'])
        global alleleList
        alleleNum = len(alleleList)
        self.ui.tw_diff.setColumnCount(5)
        self.ui.tw_diff.setRowCount(len(result['groupName']) + 1)
        # self.ui.tw_diff.setRowCount(5)

        self.ui.tw_diff.setItem(0, 0, QTableWidgetItem("groupName"))
        self.ui.tw_diff.setItem(0, 1, QTableWidgetItem("examplePair"))
        if matchMode == 0:
            self.ui.tw_diff.setItem(0, 2, QTableWidgetItem("misMatchNum"))
            self.ui.tw_diff.setItem(0, 3, QTableWidgetItem("misMatchSteps"))
            self.ui.tw_diff.setItem(0, 4, QTableWidgetItem("misMatchRatio"))
        else:
            self.ui.tw_diff.setItem(0, 2, QTableWidgetItem("matchNum"))
            self.ui.tw_diff.setItem(0, 3, QTableWidgetItem("matchSteps"))
            self.ui.tw_diff.setItem(0, 4, QTableWidgetItem("matchRatio"))
        self.ui.tw_diff.setEditTriggers(QTableWidget.NoEditTriggers)

        # for n in range(len(alleleList)):
        #     self.ui.tw_diff.setItem(0, n + 5, QTableWidgetItem(alleleList[n]))
        # #
        for i in range(self.ui.tw_diff.rowCount() - 1):
            self.ui.tw_diff.setItem(i + 1, 0, QTableWidgetItem(result['groupName'][i]))
            self.ui.tw_diff.setItem(i + 1, 1, QTableWidgetItem(result['examplePair'][i]))
            self.ui.tw_diff.setItem(i + 1, 2, QTableWidgetItem(str(result['misMatchNum'][i])))
            self.ui.tw_diff.setItem(i + 1, 3, QTableWidgetItem(str(result['misMatchSteps'][i])))
            self.ui.tw_diff.setItem(i + 1, 4, QTableWidgetItem(str(round(result['misMatchRatio'][i], 3))))
            # for j in range(alleleNum):
            #     self.ui.tw_diff.setItem(i + 1, j + 5, QTableWidgetItem(result['misMatchDetail'][i][j]))

    def showHistogram(self, result,option):
        global file
        fileName = file.split('/')[-1][0:-4]
        if option == 'same':
            histogram.setData(result,fileName,'same')
        else:
            histogram.setData(result,fileName,'diff')
    def checkMismatchMode(self):
        rb = self.sender()
        global matchMode
        if rb.isChecked() == True:
            matchMode = 0
        else:
            matchMode = 1

    def checkMatchMode(self):
        rb = self.sender()
        global matchMode
        if rb.isChecked() == True:
            matchMode = 1
        else:
            matchMode = 0
    def save(self):
        global resultDiff,resultSame,alleleList
        # both output
        if self.ui.tw_same.rowCount() > 0 and self.ui.tw_diff.rowCount() > 0:
            file,_= QFileDialog.getSaveFileName(self, "save result file", "",
                                               "Text Files ()")
            fpSame=open(file+'_same.txt','w',encoding='utf-8')
            for j in range(self.ui.tw_same.columnCount()):
                fpSame.write(self.ui.tw_same.item(0,j).text())
                fpSame.write('\t')
            for j in alleleList:
                fpSame.write(j)
                fpSame.write('\t')
            fpSame.write('\n')

            for i in range(len(resultSame['groupName'])):
                ss = resultSame['groupName'][i] + '\t' + resultSame['examplePair'][i] + '\t' + str(resultSame['misMatchNum'][i]) + '\t' + str(resultSame['misMatchSteps'][i]) + '\t' + str(round(resultSame['misMatchRatio'][i], 3)) + '\t'
                for j in range(len(resultSame['misMatchDetail'][i])):
                    ss += resultSame['misMatchDetail'][i][j]
                    ss += '\t'
                ss += '\n'
                fpSame.write(ss)

            fpDiff=open(file+'_diff.txt','w',encoding='utf-8')
            for j in range(self.ui.tw_diff.columnCount()):
                fpDiff.write(self.ui.tw_diff.item(0,j).text())
                fpDiff.write('\t')
            for j in alleleList:
                fpDiff.write(j)
                fpDiff.write('\t')
            fpDiff.write('\n')

            for i in range(len(resultDiff['groupName'])):
                ss = resultDiff['groupName'][i] + '\t' + resultDiff['examplePair'][i] + '\t' + str(
                    resultDiff['misMatchNum'][i]) + '\t' + str(resultDiff['misMatchSteps'][i]) + '\t' + str(
                    round(resultDiff['misMatchRatio'][i], 3)) + '\t'
                for j in range(len(resultDiff['misMatchDetail'][i])):
                    ss += resultDiff['misMatchDetail'][i][j]
                    ss += '\t'
                ss += '\n'
                fpDiff.write(ss)
        #
        # only same output
        elif self.ui.tw_same.rowCount()> 0 and self.ui.tw_diff.rowCount() == 0:
            file,_= QFileDialog.getSaveFileName(self, "save result file", "",
                                               "Text Files ()")
            fp = open(file + '.txt','w',encoding='utf-8')

            for j in range(self.ui.tw_same.columnCount()):
                fp.write(self.ui.tw_same.item(0,j).text())
                fp.write('\t')
            for j in alleleList:
                fp.write(j)
                fp.write('\t')
            fp.write('\n')

            for i in range(len(resultSame['groupName'])):
                ss = resultSame['groupName'][i] + '\t' + resultSame['examplePair'][i] + '\t' + str(resultSame['misMatchNum'][i]) + '\t' + str(resultSame['misMatchSteps'][i]) + '\t' + str(round(resultSame['misMatchRatio'][i], 3)) + '\t'
                for j in range(len(resultSame['misMatchDetail'][i])):
                    ss += resultSame['misMatchDetail'][i][j]
                    ss += '\t'
                ss += '\n'
                fp.write(ss)

        # only diff output
        elif self.ui.tw_same.rowCount() == 0 and self.ui.tw_diff.rowCount() >0:
            file,_= QFileDialog.getSaveFileName(self, "save result file", "",
                                               "Text Files ()")
            fp = open(file + '.txt','w',encoding='utf-8')

            for j in range(self.ui.tw_diff.columnCount()):
                fp.write(self.ui.tw_diff.item(0,j).text())
                fp.write('\t')
            for j in alleleList:
                fp.write(j)
                fp.write('\t')
            fp.write('\n')

            for i in range(len(resultDiff['groupName'])):
                ss = resultDiff['groupName'][i] + '\t' + resultDiff['examplePair'][i] + '\t' + str(
                    resultDiff['misMatchNum'][i]) + '\t' + str(resultDiff['misMatchSteps'][i]) + '\t' + str(
                    round(resultDiff['misMatchRatio'][i], 3)) + '\t'
                for j in range(len(resultDiff['misMatchDetail'][i])):
                    ss += resultDiff['misMatchDetail'][i][j]
                    ss += '\t'
                ss += '\n'
                fp.write(ss)





