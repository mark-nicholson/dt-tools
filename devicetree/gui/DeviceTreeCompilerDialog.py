
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

        self.actionPadding.triggered.connect(self.do_actionPadding)


    def do_actionPadding(self):
        print("do_actionPadding(): begin")
        self.padSpinBox.setEnabled(True)
        
