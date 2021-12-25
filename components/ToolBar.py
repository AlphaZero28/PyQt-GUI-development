from PyQt5.QtWidgets import QAction, QFileDialog, QWidget, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QImage
import fitz


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

    def set_main_view(self, cmain_view):
        self.cmain_view = cmain_view

    def openFiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open File', "")

        self.get_pages(fname[0])
        # self.mainwindow.change_label(fname[0])

    def get_pages(self, filename):
        doc = fitz.open(filename)
        no_page = len(doc)
        imgs = []

        for i in range(no_page):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            qtimg = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
            imgs.append(qtimg)

        print(type(qtimg))
        # print(imgs)
        # output = "outfile.png"
        # pix.save(output)
        # self.cmain_view.show_page(qtimg)
        self.cmain_view.set_scrollview(imgs)
