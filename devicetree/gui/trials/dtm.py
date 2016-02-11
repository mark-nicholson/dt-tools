import sys
import os
import platform

# pyside resources
from PySide import QtCore
from PySide.QtGui import *

# grab the autogen UI
from main import Ui_MainWindow


class ControlMainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, args, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.hlayout = QHBoxLayout()

        self.hlayout.addWidget( self.textEdit )
        self.hlayout.addWidget( self.graphicsView )

        self.centralwidget.setLayout(self.hlayout)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = ControlMainWindow(sys.argv)
    mySW.show()
    sys.exit(app.exec_())
