#
#  Graphical User Interface to manage Flattened Device Trees
#     Provide visual interactivity with the .dts and .dtb files
#
#  Copyright 2014 - Mark Nicholson <nicholson.mark@gmail.com>
#

import sys
import platform

import PySide
from PySide import QtCore, QtGui
from PySide.QtGui import QIcon

# grab the autogen UI
from dtgui import Ui_MainWindow

__version__ = "0.1"

#
# Multiply inherit because we mainly need to be a QMainWindow with
# some features...
#
class ControlMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.actionQuit.triggered.connect(self.close)
        self.actionQuit.setIcon(QIcon(":/quit.png"))
        self.actionQuit.setStatusTip("Close down the application.")

        self.actionAbout.triggered.connect(self.do_actionAbout)
        self.actionAbout.setIcon(QIcon(":/about.png"))
        self.actionAbout.setStatusTip("Pop up the About dialog.")

        self.actionLoad.triggered.connect(self.do_actionLoad)
        self.actionLoad.setIcon(QIcon(":/load.png"))
        self.actionLoad.setStatusTip("Pop up the Load dialog.")


    def xdo_actionLoad(self):
         MESSAGE = "<p>Message boxes have a caption, a text, and up to three " \
"buttons, each with standard or custom texts.</p>" \
"<p>Click a button to close the message box. Pressing the Esc " \
"button will activate the detected escape button (if any).</p>"
         reply = QtGui.QMessageBox.critical(self, "QMessageBox.critical()",
                                            MESSAGE,
                                            QtGui.QMessageBox.Abort | QtGui.QMessageBox.Retry | QtGui.QMessageBox.Ignore)

    def do_actionLoad(self):

        #options = QtGui.QFileDialog.Options()
        options = None
        #if not self.native.isChecked():
        #    options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "Tomato",
            "All Files (*);;Text Files (*.txt)",
            options)

        if fileName:
            #self.openFileNameLabel.setText(fileName)
            print("Got Filename: " + fileName)


    def do_actionAbout(self):
        QtGui.QMessageBox.about(self, "About PySide, Platform and version.",
                """<b> about.py version %s </b> 
                <p>Copyright &copy; 2013 by Algis Kabaila. 
                This work is made available under  the terms of
                Creative Commons Attribution-ShareAlike 3.0 license,
                http://creativecommons.org/licenses/by-sa/3.0/.
                <p>This application is useful for displaying  
                Qt version and other details.
                <p>Python %s -  PySide version %s - Qt version %s on %s""" %
                (__version__, platform.python_version(), PySide.__version__,
                 PySide.QtCore.__version__, platform.system()))                 



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

