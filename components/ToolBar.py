from PyQt5.QtWidgets import QAction, QFileDialog, QLabel, QWidget, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import fitz
import tkinter as tk


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
            self, 'Open File', "")
        self.get_pages(fname[0])
        # self.mainwindow.change_label(fname[0])
        self.mainwindow.change_label(fname[0])

    def get_pages(self, filename):
        doc = fitz.open(filename)
        page_no = 5
        page = doc.load_page(page_no)  # number of page
        pix = page.get_pixmap()
        output = "outfile"+str(page_no)+".png"
        pix.save(output)
