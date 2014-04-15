
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


class DeviceTreeCompilerDialog(QDialog, Ui_CompilerDialog):
    
    def __init__(self, args, parent=None):
        super(DeviceTreeCompilerDialog, self).__init__(parent)
        self.setupUi(self)

        # create a dtc
        self.dtc = DTC()

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

        # hook up the compilation
        self.actionCompile.triggered.connect(self.do_actionCompile)
        
    def do_actionChooseInFile(self):
        options = None
        fileName, filtr = QFileDialog.getOpenFileName(
            self,
            "Select Source Device Tree",
            "",
            "All Files (*);; DeviceTree Source (*.dts)",
            options)

        # not sure if this is possible
        if not fileName or not os.path.exists(fileName):
            QMessageBox.warning(self,
                                "File %s was not found." % fileName,
                                "Please select a valid file",
                                QMessageBox.Ok)
            return

        # update the UI
        self.dtc.in_file = fileName
        self.inFileLineEdit.setText(fileName)
        idx = self.inFileComboBox.findText(self.dtc.in_format)
        self.inFileComboBox.setCurrentIndex(idx)
        

    def do_actionChooseOutputFile(self):
        options = None
        fileName, filtr = QFileDialog.getSaveFileName(
            self,
            "Select the output file...",
            "",
            "All Files (*);; DeviceTree Binary (*.dtb)",
            options)

        # update the UItext box
        self.dtc.out_file = fileName
        self.outFileLineEdit.setText(fileName)
        idx = self.outFileComboBox.findText(self.dtc.out_format)
        self.outFileComboBox.setCurrentIndex(idx)


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
        row = self.includeListWidget.currentRow()
        item = self.includeListWidget.takeItem(row)
        self.includeListWidget.insertItem(row+1, item)

    def do_actionUpInclude(self):
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


    def do_actionCompile(self):
        print("Compiling!")

        # filenames are already loaded

        # unload the GUI params
        self.dtc.force = self.forceCheckBox.isChecked()
        self.dtc.sort = self.sortCheckBox.isChecked()

        if self.padCheckBox.isChecked():
            self.dtc.pad = self.padSpinBox.value()
        else:
            self.dtc.pad = None

        if self.reserveCheckBox.isChecked():
            self.dtc.reserve = self.reserveSpinBox.value()
        else:
            self.dtc.reserve = None

        if self.spaceCheckBox.isChecked():
            self.dtc.space = self.spaceSpinBox.value()
        else:
            self.dtc.space = None

        if self.cpuidCheckBox.isChecked():
            self.dtc.boot_cpu = self.cpuidSpinBox.value()
        else:
            self.dtc.boot_cpu = None

        phandle = self.phandleComboBox.currentText()
        if phandle != '':
            self.dtc.phandle = phandle

        # extract the include paths
        for idx in range(self.includeListWidget.count()):
            item = self.includeListWidget.item(idx)
            self.dtc.includes.append( item.text() )

        # run it
        rc, log = self.dtc.build()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = DeviceTreeCompilerDialog(sys.argv)
    dlg.show()
    sys.exit(app.exec_())
