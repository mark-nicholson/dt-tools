#
#  Graphical User Interface to manage Flattened Device Trees
#     Provide visual interactivity with the .dts and .dtb files
#
#  Copyright 2014 - Mark Nicholson <nicholson.mark@gmail.com>
#

import sys
import os
import platform

# pyside resources
from PySide import __version__ as __pyside_version__
from PySide import QtCore
from PySide.QtGui import *

# grab the autogen UI
from devicetree.gui.dt_main_window import Ui_MainWindow

# pull int FDT tools
from devicetree.dtc import DTC
from devicetree.fdt import FDT, FDTAction

from devicetree.gui.DeviceTreeCompilerDialog import DeviceTreeCompilerDialog
from devicetree.gui.ConsoleDialog import ConsoleDialog


# helpful later
__version__ = "0.1"

class DebugAction(FDTAction):
    def __init__(self, mc):
        super().__init__()
        self.depth = 0
        self.mc = mc

    def manage(self, fdt, offset, item):
        self.msg('MANAGE: ', item, offset)

    def enter(self, fdt, offset, item):
        self.depth += 1
        self.msg('ENTER: ', item, offset)
        
    def exit(self, fdt, offset, item):
        self.msg('EXIT: ', item, offset)
        self.depth -= 1

    def msg(self, text, item, offset):
        pad = '    ' * self.depth
        self.mc.log(pad + text + '%d: ' % offset + str(item))


class ModelGeneratorAction(FDTAction):
    """Action class to iterate through the FDT and generate the Model suitable for the QTreeView"""
    
    def __init__(self, modelRoot, mainWindow=None):
        super().__init__()
        self._depth = 0
        self._max_depth = 0
        self.mainWindow = mainWindow
        self.modelRoot = modelRoot
        self.stack = [ modelRoot ]
        self.max_name_width = 0
        
    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, value):
        self._depth = value
        if self._depth > self._max_depth:
            self._max_depth = self._depth

    @property
    def max_depth(self):
        return self._max_depth

    def _update_max_name_width(self, new_name):
        if len(new_name) > self.max_name_width:
            self.max_name_width = len(new_name)

    def manage(self, fdt, offset, item):
        self.msg('MANAGE: ', item, offset)
        self._update_max_name_width(item.name)
        name = QStandardItem(item.name)
        name.setData( (fdt, offset, item) )
        value = QStandardItem( item.value_text() )
        self.stack[self.depth].appendRow( [name, value] )

    def enter(self, fdt, offset, item):
        self._update_max_name_width(item.name)
        name = QStandardItem(item.name + '/')
        value = QStandardItem( item.value_text() )
        self.stack[self.depth].appendRow( [name, value] )

        # push!
        self.stack.append( name )
        self.depth += 1

        # report
        self.msg('ENTER: ', item, offset)
        
    def exit(self, fdt, offset, item):
        self.msg('EXIT: ', item, offset)
        item = self.stack.pop()
        self.depth -= 1

    def log(self, text):
        if self.mainWindow is None:
            return
        pad = '    ' * self.depth
        self.mainWindow.log(pad + text)
        
    def msg(self, text, item, offset):
        self.log(text + '%d: ' % offset + str(item))

                

#
# Multiply inherit because we mainly need to be a QMainWindow with
# some features...
#
class ControlMainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, args, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.setupUi(self)

        # adjust the tabs' layout
        self.mtabLayout = QVBoxLayout()
        self.mtabLayout.addWidget( self.memoryGraphicsView )
        self.memoryTab.setLayout( self.mtabLayout )

        self.itabLayout = QVBoxLayout()
        self.itabLayout.addWidget( self.interruptGraphicsView )
        self.interruptTab.setLayout( self.itabLayout )

        # adjust the main window layout to be proper
        #  -- the designer doesn't seem to be able to do this...
        self.hlayout = QHBoxLayout()

        self.hlayout.addWidget( self.treeView )
        self.hlayout.addWidget( self.tabWidget )

        self.centralwidget.setLayout(self.hlayout)


        # setup the console
        self.consoleDialog = ConsoleDialog(self)

        self.actionQuit.triggered.connect(self.close)
        self.actionQuit.setIcon(QIcon(":/quit.png"))
        self.actionQuit.setStatusTip("Close down the application.")

        self.actionAbout.triggered.connect(self.do_actionAbout)
        self.actionAbout.setIcon(QIcon(":/about.png"))
        self.actionAbout.setStatusTip("Pop up the About dialog.")

        self.actionLoad.triggered.connect(self.do_actionLoad)
        self.actionLoad.setIcon(QIcon(":/load.png"))
        self.actionLoad.setStatusTip("Pop up the Load dialog.")

        self.actionCompiler.triggered.connect(self.do_actionCompiler)
        self.actionCompiler.setIcon(QIcon(":/compile.png"))
        self.actionCompiler.setStatusTip("Pop up the Compile dialog.")

        self.actionConsole.triggered.connect(self.do_actionConsole)

        # placeholder for the model
        self.fdt_model = None

        # configure the tree view
        self.treeView.setModel(self.fdt_model)
        self.treeView.setUniformRowHeights(True)


    def do_actionCompiler(self):
        """Run the compilation dialog"""
        dtcompiler = DeviceTreeCompilerDialog([], self)
        dtcompiler.show()

    def do_actionConsole(self):
        self.consoleDialog.show()

    def do_actionLoad(self):
        options = None
        fileName, filtr = QFileDialog.getOpenFileName(
            self,
            "Load a Device Tree to Display ...",
            "",
            "All Files (*);; DeviceTree Source (*.dts);; DeviceTree Binary (*.dtb)",
            options)

        # not sure if this is possible
        if not fileName or not os.path.exists(fileName):
            QMessageBox.warning(self,
                                "File %s was not found." % fileName,
                                "Please select a valid file",
                                QMessageBox.Ok)
            return

        # if it is a DTS file, compile it
        if fileName.endswith('.dts'):
            print("Need to compile DTS into DTB...")
            return

        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeView.setUniformRowHeights(True)

        # try to parse it
        self.fdt = FDT(fileName)

        # create the model
        self.fdt_model = QStandardItemModel()
        self.fdt_model.setHorizontalHeaderLabels(['Name', 'Value'])
        self.treeView.setModel(self.fdt_model)

        # create top level item
        root = QStandardItem(os.path.basename(fileName))
        emptyItem = QStandardItem('')
        self.fdt_model.appendRow( [ root, emptyItem ] )
        
        # put in the header
        header = QStandardItem('Header')
        for field in self.fdt.header._fields:
            item = QStandardItem(field)
            value = QStandardItem(str(getattr(self.fdt.header, field)))
            header.appendRow( [ item, value ] )

        emptyItem = QStandardItem('')
        root.appendRow( [ header, emptyItem ] )

        # iterate over the tree
        action = ModelGeneratorAction(root, self)
        self.fdt.walk(action)

        print("Max Name:  %d" % action.max_name_width)
        print("Max Depth: %d" % action.max_depth)

        # make sure the root is expanded
        r_idx = self.fdt_model.indexFromItem(root)
        self.treeView.expand(r_idx)

        # expand the top level entries by default...
        for idx in range(root.rowCount()):
            item = root.child(idx, 0)
            tidx = self.fdt_model.indexFromItem(item)
            self.treeView.expand(tidx)
        
        # make the name column wide enough
        self.treeView.resizeColumnToContents(0)

        # display it
        self.treeView.show()


    def do_actionAbout(self):
        QMessageBox.about(self, "Device Tree Viewer",
                """<h3> dtviewer.py version %s </h3> 
                <p>Copyright &copy; 2014 by Mark Nicholson. 
                This work is made available under  the terms of BSDv3 license.
                <p>This application provides a visual interface to work with
                Flattened Device Tree files and their details.
                <h3>Versions:</h3>
                <ul>
                <li>Python %s
                <li>PySide version %s
                <li>Qt version %s
                <li>Host OS: %s
                </ul>""" %
                (__version__, platform.python_version(), __pyside_version__,
                 QtCore.__version__, platform.system()))                 

    def log(self, data):
        console = self.consoleDialog
        console.log(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = ControlMainWindow(sys.argv)
    mySW.show()
    sys.exit(app.exec_())

