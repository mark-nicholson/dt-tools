#!/usr/bin/env python3

# PyQt tutorial 5


import sys
from PySide import QtCore, QtGui

from devicetree.AddressMap import AddressMapItem

        
class UtilityWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        quit = QtGui.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        lcd = QtGui.QLCDNumber(2)

        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(0)

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))

        p1 = QtGui.QPalette(QtGui.QColor(250, 250, 200))
        ae1 = AddressMapItem(0x12000, 0x4000, "I2C", p1)

        p2 = QtGui.QPalette(QtGui.QColor(150, 150, 100))
        ae2 = AddressMapItem(0x40000, 0x10000, "PCI", p2)

        p3 = QtGui.QPalette(QtGui.QColor(250, 250, 200))
        ae3 = AddressMapItem(0x8000000, 0x400000, "RAM", p3)

        p4 = QtGui.QPalette(QtGui.QColor(150, 150, 100))
        ae4 = AddressMapItem(0x0, 0x80, "SPI", p4)
        
        layout = QtGui.QVBoxLayout()
        layout.layoutSpacing = 0
        layout.addWidget(quit)
        layout.addWidget(ae1)
        layout.addWidget(ae2)
        layout.addWidget(ae3)
        layout.addWidget(ae4)
        self.setLayout(layout)


app = QtGui.QApplication(sys.argv)
widget = UtilityWidget()
widget.show()
sys.exit(app.exec_())
