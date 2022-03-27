from PIL import Image
from PyQt5.QtWidgets import QAction, QFileDialog, QWidget, QToolBar,QSpinBox, QLabel
from PyQt5 import QtCore,Qt
from PyQt5.QtGui import QIcon, QImage
import fitz
# from matplotlib import style
from components.ImageProcessing import imgProcess
from components.config import debug
from docx import Document
from docx.shared import Pt 



class cToolBar(QWidget):
    def __init__(self, mainwindow):
        super(cToolBar, self).__init__()
        self.mainwindow = mainwindow
        self.zoom = 1

        # file toolbar
        fileToolBar = QToolBar("File", self)
        fileToolBar.setIconSize(QtCore.QSize(30, 30))

        openActionForToolBar = QAction(
            QIcon('./assets/file.png'), "&Open", self)
        openActionForToolBar.triggered.connect(self.openFiles)

        saveActionForToolBar = QAction(
            QIcon('./assets/save-solid.svg'), "&Save", self)
        saveActionForToolBar.triggered.connect(self.saveFiles)
        

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



        # navigation toolbar
        # add label for navigation
        label = QLabel()
        label.setText('GoTo')

        # add spinbox for navigation
        self.navigationBox = QSpinBox()
        # navigationBox.setFocusPolicy(Qt.NoFocus)
        self.navigationBox.valueChanged.connect(self.navigationFunction)

        navigationBar = QToolBar("Navigation", self)
        navigationBar.addWidget(label)
        navigationBar.addWidget(self.navigationBox)
        

        # add toolbar to mainwindow
        self.mainwindow.addToolBar(fileToolBar)
        self.mainwindow.addToolBar(viewToolBar)
        self.mainwindow.addToolBar(navigationBar)
        

    def navigationFunction(self):
        page_number = self.navigationBox.value()
        self.cmain_view.goto_specific_page(page_number)

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
        if debug:
            name = r'math-book-9-10-9-12.pdf'
            imgs = imgProcess.get_pages(name)
            self.cmain_view.set_imgs(imgs)
            return

        fname = QFileDialog.getOpenFileName(
            self, 'Open File', "", "PDF files (*.pdf);;")
        
        if fname[0]=='':
            return

        # self.get_pages(fname[0])
        self.imgs = imgProcess.get_pages(fname[0])
        self.cmain_view.set_imgs(self.imgs)
        # self.mainwindow.change_label(fname[0])


    def saveFiles(self):
        no_of_pages = len(self.imgs)

        # file = str(QFileDialog.get)
        file = QFileDialog.getSaveFileName(self)
        filename = file[0]

        print(type(file))

        # pages = []
        document = Document()
        style = document.styles['Normal']
        font = style.font
        font.name  = 'Arial'
        font.size = Pt(12)

        for i in range(no_of_pages):
            [tempQW, page] = self.cmain_view.create_page(self.imgs[i]) 
            paragraph = document.add_paragraph(' ')
            paragraph.style = document.styles['Normal']
            for line in page:
                paragraph.add_run(line)
                paragraph.add_run('\n')
            
            document.add_page_break()
        document.save(filename)


        # with open('sample.txt', 'a') as f:
        #     for line in txt:
        #         f.write('\n')
        #         f.write(line)




