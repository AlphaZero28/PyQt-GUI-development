from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from MenuBar import cMenuBar # custom menubar
from ToolBar import cToolBar # custom toolbar


class GUIMainWindow(QMainWindow):
    def __init__(self):
        super(GUIMainWindow, self).__init__()
        
        self.setWindowTitle("Accessible PDF Reader")
        self.setGeometry(50, 50, 1000, 900)

        # initializing menubar and toolbar
        self.cmenu_bar = cMenuBar(self)
        self.ctool_bar = cToolBar(self)

        # initializing main windows UI
        self.initUI()


    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("first label")
        self.label.move(100, 300)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("click")
        # self.b1.clicked.connect(self.clicked)
        self.b1.move(100, 100)

    def change_label(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()