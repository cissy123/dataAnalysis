# -*- coding: utf-8 -*-
import numpy as np
from collections import defaultdict
import os

import matplotlib as mpl

mpl.use('Qt5Agg')
import matplotlib.pyplot as plt


def setData(result,fileName,option):
    plt.close('all')
    # print(result)
    if option == 'same':
        path = clearFolder(fileName,'same')
        
    else:
        path = clearFolder(fileName,'different')

    r = np.unique(result['groupName'])
    num = 0
    hisDict = defaultdict(list)
    for i in r:
        hisDict['groupName'].append(i)
        dataList = list()
        for j in result['groupName']:
            if j == i:
                dataList.append(result['misMatchNum'][num])
                num += 1
        hisDict['hisData'].append(dataList)
    #wriet 00_index.txt to login the groupPairName
    fp = open(os.path.join(path,'00_index.txt'),'w',encoding='utf-8')

    x_axes = len(result['misMatchDetail'][0])
    for i in range(len(hisDict['groupName'])):
        #write index
        string = str(i) + '\t' + hisDict['groupName'][i] + '\n'
        fp.write(string)

        #count histogram count
        count = list()
        for j in range(x_axes):
            count.append(hisDict['hisData'][i].count(j))

        figure = plt.figure(i)
        plt.bar(x=range(x_axes), height=count)

        figname = str(str(i) + '_' + hisDict['groupName'][i]) + '.png'
        specialCharacter = ['*','/']
        for x in specialCharacter:
            if x in figname:
                figname = figname.replace(x, "_")
        dest = os.path.join(path, figname)
        plt.savefig(dest)  # write image to file
        plt.close(figure)
        plt.clf()
def clearFolder(fileName,path):
    path = os.path.join('figures',fileName,path)
    if os.path.exists(path):
        for i in os.listdir(path):
            path_file = os.path.join(path,i)
            if os.path.isfile(path_file):
                os.remove(path_file)
    else:
        os.makedirs(path)
    return path