#! /usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In this prototype/example a QTreeView is created. Then it's populated with
# three containers and all containers are populated with three rows, each
# containing three columns.
# Then the last container is expanded and the last row is selected.
# The container items are spanned through the all columns.
# Note: this requires > python-3.2
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys, os, pprint, time
from PySide.QtCore import *
from PySide.QtGui import *
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
app = QApplication(sys.argv)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# init widgets
class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.listWidget = QListWidget()
        self.tableWidget = QTableWidget(3, 1, self)
        self.textEdit = QTextEdit()
        self.frame = QFrame()

        self.button2 = QPushButton("Orange")
        leftSpacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.button3 = QPushButton("Pear")
        #self.button4 = QPushButton("Apple")
        #self.button5 = QPushButton("Banana")

        self.frame_layout = QHBoxLayout()
        self.frame_layout.insertStretch(0)
        self.frame_layout.addWidget(self.button2)
        self.frame_layout.insertStretch(-1)
        #self.frame_layout.addWidget(self.button3)
        #self.frame_layout.addWidget(self.button4)
        #self.frame_layout.addWidget(self.button5)

        self.frame.setLayout(self.frame_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.frame)

        self.setLayout(layout)

        item1 = QListWidgetItem("Hello")
        item2 = QListWidgetItem("World")
        item3 = QListWidgetItem("!")

        self.listWidget.addItem( item1 )
        self.listWidget.addItem( item2 )
        self.listWidget.addItem( item3 )
        self.listWidget.selectionRectVisible = True

        t1 = QTableWidgetItem( "Table Entry 1" )
        t2 = QTableWidgetItem( "Table Entry 2" )
        t3 = QTableWidgetItem( "Table Entry 3" )
        self.tableWidget.setItem( 0, 0, t1 )
        self.tableWidget.setItem( 1, 0, t2 )
        self.tableWidget.setItem( 2, 0, t3 )
        
dlg = MyDialog()
dlg.show()

# view = QTreeView()
# view.setSelectionBehavior(QAbstractItemView.SelectRows)
# model = QStandardItemModel()
# model.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
# view.setModel(model)
# view.setUniformRowHeights(True)
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # populate data
# for i in range(3):
#     parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
#     for j in range(3):
#         child1 = QStandardItem('Child {}'.format(i*3+j))
#         child2 = QStandardItem('row: {}, col: {}'.format(i, j+1))
#         child3 = QStandardItem('row: {}, col: {}'.format(i, j+2))
#         parent1.appendRow([child1, child2, child3])
#     model.appendRow(parent1)
#     # span container columns
#     view.setFirstColumnSpanned(i, view.rootIndex(), True)
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # expand third container
# index = model.indexFromItem(parent1)
# view.expand(index)
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # select last row
# selmod = view.selectionModel()
# index2 = model.indexFromItem(child3)
# selmod.select(index2, QItemSelectionModel.Select|QItemSelectionModel.Rows)
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# view.show()
sys.exit(app.exec_())
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
