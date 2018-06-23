from collections import defaultdict
from PyQt5 import QtCore

from PyQt5.QtWidgets import QDialog,QTreeWidgetItem
from ui_groupWidget import Ui_groupWidget

class groupWidget(QDialog):
    def __init__(self):
        super(groupWidget, self).__init__()
        self.ui = Ui_groupWidget()
        self.ui.setupUi(self)
        self.ui.tw_same.itemChanged.connect(self.treeItemChangedSame)
        self.ui.tw_diff.itemChanged.connect(self.treeItemChangedDiff)

    def buildTree(self,groupName):
        ## same ##
        itemSame = QTreeWidgetItem(self.ui.tw_same)
        itemSame.setFlags(itemSame.flags())
        itemSame.setText(0, "AllSelect")
        itemSame.setCheckState(0,QtCore.Qt.Unchecked)
        for i in range(len(groupName)):
            item = QTreeWidgetItem(itemSame)
            item.setFlags(item.flags())
            item.setText(0, str(groupName[i]))
            item.setCheckState(0,QtCore.Qt.Unchecked)

        ## diff ##

        itemDiff = QTreeWidgetItem(self.ui.tw_diff)
        itemDiff.setFlags(itemDiff.flags())
        itemDiff.setText(0, "AllSelect")
        itemDiff.setCheckState(0,QtCore.Qt.Unchecked)
        for i in range(len(groupName)):
            item = QTreeWidgetItem(itemDiff)
            item.setFlags(item.flags())
            item.setText(0, str(groupName[i]))
            item.setCheckState(0,QtCore.Qt.Unchecked)


    def updateTreeStatus(self,root):
        mapping = defaultdict(list)
        # pp = root.parent()
        # print(pp)
        for index in range(root.childCount()):
            parent = root.child(index)

            if parent.checkState(0) == QtCore.Qt.Unchecked:
                features = mapping[parent.text(0)]
                for row in range(parent.childCount()):
                    child = parent.child(row)
                    if child.checkState(0) == QtCore.Qt.Checked:
                        features.append(child.text(0))

            elif parent.checkState(0) == QtCore.Qt.Checked:
                features = mapping[parent.text(0)]
                for row in range(parent.childCount()):
                    child = parent.child(row)
                    features.append(child.text(0))
                    child.setCheckState(0,QtCore.Qt.Checked)

        return mapping

    def treeItemChangedSame(self):
        root = self.ui.tw_same.invisibleRootItem()
        mapping = self.updateTreeStatus(root)
        return mapping

    def treeItemChangedDiff(self):
        root = self.ui.tw_diff.invisibleRootItem()
        mapping = self.updateTreeStatus(root)
        return mapping




 