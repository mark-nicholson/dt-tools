
import sys
import os
import platform

# pyside resources
from PySide import QtCore
from PySide.QtGui import *

# grab the autogen UI
from compiler_dialog import Ui_CompilerDialog

# pull int FDT tools
from devicetree.dtc import DTC
from devicetree.fdt import FDT, FDTAction

class DeviceTreeCompilerDialog(QDialog, Ui_CompilerDialog):
    
    def __init__(self, args, parent=None):
        super(DeviceTreeCompilerDialog, self).__init__(parent)
        self.setupUi(self)

        # load some data
        self.phandleComboBox.addItems( DTC._phandle_choices )
        self.inFileComboBox.addItems( DTC._format_choices )
        self.outFileComboBox.addItems( DTC._format_choices )

        # setup some button actions
        self.actionChooseInFile.triggered.connect(self.do_actionChooseInFile)
        self.actionChooseOutputFile.triggered.connect(self.do_actionChooseOutputFile)

        # manage includes
        self.actionAddInclude.triggered.connect(self.do_actionAddInclude)
        self.actionDownInclude.triggered.connect(self.do_actionDownInclude)
        self.actionRemoveInclude.triggered.connect(self.do_actionRemoveInclude)
        self.actionUpInclude.triggered.connect(self.do_actionUpInclude)
        self.actionIncludeSelected.triggered.connect(self.do_actionIncludeSelected)

        
    def do_actionChooseInFile(self):
        options = None
        fileName, filtr = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "Tomato",
            "All Files (*);; DeviceTree Source (*.dts);; DeviceTree Binary (*.dtb)",
            options)

        # not sure if this is possible
        if not fileName or not os.path.exists(fileName):
            QMessageBox.warning(self, "File %s was not found." % fileName, "Please select a valid file",
                                      QMessageBox.Ok)
            return

        # update the text box
        self.inFileLineEdit.setText(fileName)
        

    def do_actionChooseOutputFile(self):
        options = None
        fileName, filtr = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "Tomato",
            "All Files (*);; DeviceTree Binary (*.dtb)",
            options)

        # update the text box
        self.outFileLineEdit.setText(fileName)


    def do_actionAddInclude(self):
        options = None
        dirName = QFileDialog.getExistingDirectory(self,
                                                   "Select Include Directory",
                                                   "")

        # not sure if this is possible
        if not dirName or not os.path.exists(dirName):
            QMessageBox.warning(self, "File %s was not found." % fileName, "Please select a valid file",
                                      QMessageBox.Ok)
            return

        # update the text box
        self.includeListWidget.addItem( dirName )
        

    #
    #  Manage the movement of the entries
    #
    def do_actionDownInclude(self):
        print("In DownInclude")
        row = self.includeListWidget.currentRow()
        item = self.includeListWidget.takeItem(row)
        self.includeListWidget.insertItem(row+1, item)

    def do_actionUpInclude(self):
        print("In UpInclude")
        row = self.includeListWidget.currentRow()
        item = self.includeListWidget.takeItem(row)
        self.includeListWidget.insertItem(row-1, item)

    def do_actionRemoveInclude(self):
        row = self.includeListWidget.currentRow()
        item = self.includeListWidget.takeItem(row)
        
    def do_actionIncludeSelected(self):
        row = self.includeListWidget.currentRow()
        count = self.includeListWidget.count()

        if row < (count - 1) and (count > 1):
            self.includeDownButton.setEnabled(True)
        else:
            self.includeDownButton.setEnabled(False)
            
        if row > 0 and (count > 1):
            self.includeUpButton.setEnabled(True)
        else:
            self.includeUpButton.setEnabled(False)

        self.includeRemoveButton.setEnabled(True)
