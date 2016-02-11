#!/usr/bin/env python3

import sys
from PySide       import QtCore
from PySide.QtGui import *

#class MyProxyModel(QAbstractProxyModel):
class MyProxyModel(QSortFilterProxyModel):
    """A hack towards a proxy model"""

    def __init__(self, parent=None):
        #QAbstractProxyModel.__init__(self, parent)
        QSortFilterProxyModel.__init__(self, parent)
        
    #def mapFromSource(self, sourceIndex):
    #    """return QModelIndex
    #    arg: QModelIndex"""
    #    return sourceIndex

    #def mapToSource(self, proxyIndex):
    #    """return QModelIndex
    #    arg: QModelIndex"""
    #    return proxyIndex
    
    #def mapSelectionFromSource(self, sourceSelection):
    #    """return QItemSelection
    #    arg: QItemSelection"""
    #    return sourceSelection
    
    #def mapSelectionToSource(self, proxySelection):
    #    """return QItemSelection
    #    arg: QItemSelection"""
    #    return proxySelection
    
    #def setSourceModel(self, sourceModel):
    #    QSortFilterProxyModel.setSourceModel(self, sourceModel)
    #    self.srcModel = sourceModel
    
    #def sourceModel(self):
    #    return self.srcModel

startPath = '/'
app = QApplication(sys.argv)

splitter = QSplitter()
model = QFileSystemModel(app)
model.setRootPath(startPath)

#proxy = QSortFilterProxyModel(app)
proxy = MyProxyModel(app)
proxy.setSourceModel(model)
cmodel = proxy

treeView = QTreeView(splitter)
treeView.setModel(cmodel)
#treeView.setRootIndex(model.index(startPath))

listView = QListView(splitter)
listView.setModel(cmodel)
#listView.setRootIndex(model.index(startPath))

selection = QItemSelectionModel(cmodel)
treeView.setSelectionModel(selection)
listView.setSelectionModel(selection)

splitter.setWindowTitle('Two way viewer')
splitter.show()

sys.exit(app.exec_())

