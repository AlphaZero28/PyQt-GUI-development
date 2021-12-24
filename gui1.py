from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QFileDialog, QMenu
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtGui import QIcon
import sys
import os


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.setWindowTitle("Accessible PDF Reader")
        self.setGeometry(50, 50, 1000, 900)

        self.menuBarFunction()

        fileToolBar = QtWidgets.QToolBar("File", self)
        fileToolBar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(fileToolBar)
        # fileToolBar = self.addToolBar("File")
        openActionForToolBar = QAction(
            QIcon('accessible/assets/file.png'), "&Open", self)
        openActionForToolBar.triggered.connect(self.openFiles)

        fileToolBar.addAction(openActionForToolBar)
        saveActionForToolBar = QAction(
            QIcon('accessible/assets/save-solid.svg'), "&Save", self)
        fileToolBar.addAction(saveActionForToolBar)

        viewToolBar = self.addToolBar("View")
        minusActionForToolBar = QAction(
            QIcon('accessible/assets/minus.png'), "minus", self)
        viewToolBar.addAction(minusActionForToolBar)
        plusActionForToolBar = QAction(
            QIcon('accessible/assets/plus.png'), "&plus", self)
        viewToolBar.addAction(plusActionForToolBar)

    def menuBarFunction(self):
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('&File')
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openFiles)
        fileMenu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        fileMenu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.triggered.connect(lambda: QApplication(sys.argv))
        fileMenu.addAction(exit_action)

        editMenu = self.menuBar.addMenu('Edit')
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        editMenu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        editMenu.addAction(paste_action)

        viewMenu = self.menuBar.addMenu('View')
        zoom_action = QAction('Zoom', self)
        viewMenu.addAction(zoom_action)

        Goto_action = QAction('Goto', self)
        viewMenu.addAction(Goto_action)

        toolsMenu = self.menuBar.addMenu('Tools')

        helpMenu = self.menuBar.addMenu('Help')
        about_action = QAction('About', self)
        helpMenu.addAction(about_action)

        userGuide_action = QAction('User Guide', self)
        helpMenu.addAction(userGuide_action)

    def initUI(self):

        self.label = QtWidgets.QLabel(self)
        self.label.setText("first label")
        self.label.move(100, 300)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("click")
        # self.b1.clicked.connect(self.clicked)
        self.b1.move(100, 100)

    def openFiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', "")
        self.label.setText(fname[0])
        self.label.adjustSize()


def window():
    # os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
# print('hello')
