from PIL import Image
from PyQt5.QtWidgets import QAction, QFileDialog, QWidget, QToolBar
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QImage
import fitz
from components.ImageProcessing import imgProcess


class cToolBar(QWidget):
    def __init__(self, mainwindow):
        super(cToolBar, self).__init__()
        self.mainwindow = mainwindow
        self.imgProcess = imgProcess()
        self.zoom = 1

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
            QIcon('./assets/minus.png'), "&Zoom Out", self)
        minusActionForToolBar.triggered.connect(self.zoom_out)

        plusActionForToolBar = QAction(
            QIcon('./assets/plus.png'), "&Zoom In", self)
        plusActionForToolBar.triggered.connect(self.zoom_in)

        viewToolBar.addAction(minusActionForToolBar)
        viewToolBar.addAction(plusActionForToolBar)

        self.mainwindow.addToolBar(fileToolBar)
        self.mainwindow.addToolBar(viewToolBar)

    def set_main_view(self, cmain_view):
        self.cmain_view = cmain_view
        # self.get_pages('F:/My_Folder/__Projects__/InnovationGarage/Accessible-PDF-Reader/App/pyqt-pdfreader/Jhora Palok By Jibanananda Das (BDeBooks.Com)-pages-deleted.pdf')

    def zoom_in(self):
        self.zoom = self.zoom + 0.25
        self.cmain_view.set_zoom(self.zoom)

    def zoom_out(self):
        self.zoom = self.zoom - 0.25
        self.cmain_view.set_zoom(self.zoom)

    def openFiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open File', "")

        # self.get_pages(fname[0])
        imgs = self.imgProcess.get_pages(fname[0])
        self.cmain_view.set_imgs(imgs)
        # self.mainwindow.change_label(fname[0])

    # def get_pages(self, filename):
    #     # images = convert_from_path(filename)
    #     # print(images[0])
    #     doc = fitz.open(filename)
    #     no_page = len(doc)
    #     imgs = []
    #     zoom = 4   # zoom factor
    #     mat = fitz.Matrix(zoom, zoom)
    #     for i in range(no_page):
    #         page = doc.load_page(i)
    #         pix = page.get_pixmap(matrix=mat)
    #         pix.set_dpi(5000, 7200)
    #         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #         imgs.append(img)

        # return imgs
        # print(imgs)
        # output = "outfile.png"
        # pix.save(output)
        # self.cmain_view.show_page(qtimg)
        # self.cmain_view.set_imgs(imgs)
        # self.cmain_view.show_page(self.zoom, imgs)
        # self.cmain_view.set_single_view(imgs[0])
