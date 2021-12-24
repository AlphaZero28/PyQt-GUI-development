from PyQt5.QtWidgets import QAction, QFileDialog, QWidget, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

class cToolBar(QWidget):
    def __init__(self, mainwindow):
        super(cToolBar, self).__init__()
        self.mainwindow = mainwindow

        # file toolbar
        fileToolBar = QToolBar("File", self)
        fileToolBar.setIconSize(QtCore.QSize(30, 30))
        
        openActionForToolBar = QAction(
            QIcon('./assets/file.png'), "&Open", self)
        openActionForToolBar.triggered.connect(self.openFiles)
        saveActionForToolBar = QAction(
            QIcon('./assets/save-solid.svg'), "&Save", self)
        
        fileToolBar.addAction(openActionForToolBar)
        fileToolBar.addAction(saveActionForToolBar)

        # view toolbar
        viewToolBar = QToolBar("View", self)
        
        minusActionForToolBar = QAction(
            QIcon('./assets/minus.png'), "minus", self)
        plusActionForToolBar = QAction(
            QIcon('./assets/plus.png'), "&plus", self)

        viewToolBar.addAction(minusActionForToolBar)
        viewToolBar.addAction(plusActionForToolBar)

        self.mainwindow.addToolBar(fileToolBar)
        self.mainwindow.addToolBar(viewToolBar)
        
    def openFiles(self):
        fname = QFileDialog.getOpenFileName(
            self,'Open File', "")
        self.mainwindow.change_label(fname[0])
