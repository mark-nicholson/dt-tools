
from PySide.QtCore import Qt, QSize, QMargins
from PySide.QtGui  import *

#class AddressMapItem(QListWidgetItem):
class AddressMapItem(QWidget):
    def __init__(self, base, size, title, palette, parent=None):
        #QListWidgetItem.__init__(self, parent)
        QWidget.__init__(self, parent)

        # remember the palette used to group these
        self.palette = palette

        # setup the title label and its position
        self.title = title
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)

        # setup the address tag
        self.address = base
        self.addressLabel = QLabel("0x%x" % self.address)
        self.addressLabel.setAlignment(Qt.AlignBottom|Qt.AlignRight)

        # setup the size tag
        self.size = size
        self.sizeLabel = QLabel("0x%x" % self.size)

        # create a frame to represent the block
        self.frame = QFrame()
        self.frame.setMinimumSize(QSize(200, 100))
        self.frame.setPalette(self.palette)
        self.frame.setAutoFillBackground(True)
        self.frame.setLineWidth(1)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)

        margins = QMargins()
        margins.setTop(0)
        margins.setBottom(0)
        #self.setContentsMargins(margins)

        
        self.frameLayout = QHBoxLayout()
        self.frameLayout.addWidget(self.titleLabel)
        self.frame.setLayout(self.frameLayout)

        # arrange the pieces correctly
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.addressLabel)
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.sizeLabel)
        
        self.setLayout(self.layout)



class AddressMap(QWidget):
    """ A overall widget to display the full maps"""
    pass
