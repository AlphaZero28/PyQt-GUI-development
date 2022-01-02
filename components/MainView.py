from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QImage
from fitz.fitz import PDF_SIGNATURE_ERROR_DIGEST_FAILURE, Pixmap
from components.ToolBar import cToolBar


class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.mainwindow = mainwindow
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.imgs = []
        self.zoom = 1
        self.page_num = 0
        self.run_count = 0

        self.vbox_layout.addWidget(self.scroll_area, 10)

        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

    def set_zoom(self, value):
        self.zoom = value
        # self.show_page(self.imgs)
        self.show_single_page(self.imgs[0])
        # print(self.zoom)

    def set_imgs(self, imgs):
        self.imgs = imgs
        # self.show_page(self.imgs)
        self.page_num = 0
        self.goto_page(self.page_num)

    def goto_next_page(self):
        if not self.page_num==len(self.imgs)-1:
            self.page_num = self.page_num+1
            self.goto_page(self.page_num)
    
    def goto_prev_page(self):
        if not self.page_num==0:
            self.page_num = self.page_num-1
            self.goto_page(self.page_num)
    
    def goto_page(self, page_num):
        self.show_single_page(self.imgs[page_num])

    def show_single_page(self, img):
        self.run_count = self.run_count+1

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        groupBox = QGroupBox()  # groupBox will contain the formLayout of the pages
        form_layout = QFormLayout()

        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(0)

        no_page = len(self.imgs)

        tempQW = self.create_page(img)
        form_layout.addRow(tempQW)
        groupBox.setLayout(form_layout)

        scroll_area.setWidget(groupBox)

        self.vbox_layout.replaceWidget(self.scroll_area, scroll_area)
        self.scroll_area = scroll_area


    def show_page(self, imgs):

        self.run_count = self.run_count+1

        self.groupBox.layout().removeItem(self.form_layout)

        # FORM LAYOUT will contain the labels
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setVerticalSpacing(10)

        no_page = len(self.imgs)

        # adding the PAGES as labels to form_layout
        for i in range(no_page):
            tempQW = self.create_page(self.imgs[i])
            # self.create_page(self.imgs[i])
            self.form_layout.addRow(tempQW)

        self.groupBox.setLayout(self.form_layout)



    def create_page(self, img):

        container = QWidget()
        container.setStyleSheet('background: white;')
        page_width = QtWidgets.QDesktopWidget().screenGeometry().width()-3*80
        page_height = self.scroll_area.height()
        # page_height =  QtWidgets.QDesktopWidget().screenGeometry().height()

        # container.setFixedHeight(page_height)

        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setXOffset(0)
        effect.setYOffset(0)

        container.setGraphicsEffect(effect)
        label = QLabel(container)
        label.setText("first label")
        # label.setStyleSheet('border: 3px solid gray')

        # adding pixmap
        img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
        # pixMap = QPixmap.fromImage(img)
        pixMap = QPixmap(qim)

        aspct_ratio = pixMap.height()/pixMap.width()

        # label.setPixmap(pixMap)
        pixMap = pixMap.scaled(page_width,
                               page_height*self.zoom, Qt.KeepAspectRatio)
        # print(self.zoom)

        label.setGeometry(QRect(0, 0, pixMap.width(), pixMap.height()))

        container.setFixedWidth(pixMap.size().width())
        container.setFixedHeight(pixMap.size().height())

        label.setPixmap(pixMap)
        # label.adjustSize()
        # container.adjustSize()

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0, 0, 0, 0)
        hbox_temp.addItem(self.verticalSpacer)
        hbox_temp.addWidget(container)
        hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget(self)

        tempQW.setLayout(hbox_temp)

        return tempQW
