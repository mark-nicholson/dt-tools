# common bits
import sys

# pyside resources
from PySide import QtCore
from PySide.QtGui import *

# grab the autogen UI
from console_dialog import Ui_ConsoleDialog

class ConsoleDialog(QDialog, Ui_ConsoleDialog):
    
    def __init__(self, args, parent=None):
        super(ConsoleDialog, self).__init__(parent)
        self.setupUi(self)

        # adjust the layout to be proper -- the designer doesn't seem to be able to do this...
        self.layout = QVBoxLayout()

        self.layout.addWidget( self.textEdit )
        self.layout.addWidget( self.horizontalLayoutWidget )

        self.setLayout(self.layout)

        # line number
        self.lines = 0

        # cook up the param
        self.textEdit.setReadOnly( True )

    def log(self, data):
        self.textEdit.append(data)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = ConsoleDialog(sys.argv)
    dlg.show()
    sys.exit(app.exec_())
