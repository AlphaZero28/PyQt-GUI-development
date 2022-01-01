from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QImage
from fitz.fitz import Pixmap
from components.ToolBar import cToolBar


class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.hbox_temp = QHBoxLayout()
        self.container = QWidget()
        self.mainwindow = mainwindow
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.imgs = []
        self.zoom = 1
        self.run_count = 0
        self.get_vbox_layout(self.vbox_layout)

        self.groupBox = QGroupBox()  # groupBox will contain the formLayout of the pages
        self.form_layout = QFormLayout()
        self.groupBox.setLayout(self.form_layout)
        self.label = QLabel()

        self.scroll_area.setWidget(self.groupBox)

        self.vbox_layout.addWidget(self.scroll_area, 10)

        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

    def get_vbox_layout(self, vbox_layout):
        self.vbox_layout = vbox_layout

    def get_nextPage(self, test):
        # print(test)
        pass

    def get_zoom(self, value):
        self.zoom = value
        self.show_page(self.imgs)
        # print(self.zoom)

    def get_imgs(self, imgs):
        self.imgs = imgs
        self.show_page(self.imgs)

    def show_page(self, imgs):

        self.run_count = self.run_count+1
        #     for i in reversed(range(layout.count())):
        # layout.itemAt(i).widget().setParent(None)
        # if (self.run_count > 1):
        #     for i in reversed(range(self.vbox_layout.count())):
        #         widget_clr = self.vbox_layout.takeAt(i).widget()
        #         # print(self.vbox_layout.itemAt(i).widget())
        #         # print(self.run_count)
        #         # print('test widget')
        #         # print(widget_clr)
        #         # print(i)
        #         if widget_clr is not None:
        #             widget_clr.setParent(None)

        #     print('this is there')

        # print(self.vbox_layout.itemAt(i).widget())

        # self.vbox_layout.addWidget(self.scroll_area, 10)
        # self.vbox_layout.addWidget(self.scroll_area, 10)

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
        # print('scroll height:', self.scroll_area.height())

    # def set_scrollview(self, imgs):
    #     self.imgs = imgs

    #     # FORM LAYOUT will contain the labels
    #     form_layout = QFormLayout()
    #     form_layout.setContentsMargins(0, 0, 0, 0)
    #     form_layout.setVerticalSpacing(10)

    #     no_page = len(self.imgs)

    #     # adding the PAGES as labels to form_layout
    #     for i in range(no_page):
    #         tempQW = self.create_page(self.imgs[i])
    #         form_layout.addRow(tempQW)

    #     self.groupBox.setLayout(form_layout)
    #     print('scroll height:', self.scroll_area.height())

    def create_page(self, img):

        self.container = QWidget()
        self.container.setStyleSheet('background: white;')
        page_width = QtWidgets.QDesktopWidget().screenGeometry().width()-3*80
        page_height = self.scroll_area.height()
        # page_height =  QtWidgets.QDesktopWidget().screenGeometry().height()

        # container.setFixedHeight(page_height)

        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setXOffset(0)
        effect.setYOffset(0)

        self.container.setGraphicsEffect(effect)
        self.label = QLabel(self.container)
        self.label.setText("first label")
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

        self.label.setGeometry(QRect(0, 0, pixMap.width(), pixMap.height()))

        self.container.setFixedWidth(pixMap.size().width())
        self.container.setFixedHeight(pixMap.size().height())

        self.label.setPixmap(pixMap)
        # label.adjustSize()
        # container.adjustSize()

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        self.hbox_temp = QHBoxLayout()
        self.hbox_temp.setContentsMargins(0, 0, 0, 0)
        self.hbox_temp.addItem(self.verticalSpacer)
        self.hbox_temp.addWidget(self.container)
        self.hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget(self)

        tempQW.setLayout(self.hbox_temp)

        return tempQW

    # def zoomIn_or_zoomOut(self,value):

    #     pixmap = pixMap.scaled(page_width,page_height,Qt.KeepAspectRatio)

    # def show_page(self, qtimg):
    #     self.page_height = qtimg.height()
    #     print(self.page_height)
    #     pixMap = QPixmap.fromImage(qtimg)
    #     # pixMap = QPixmap(output)
    #     self.label.setPixmap(pixMap)
    #     self.label.adjustSize()

    # def set_container(self):
    #     # creating a HORIZONTAL LAYOUT to add to the vertical layout
    #     hbox = QHBoxLayout()
    #     hbox.setContentsMargins(0, 0, 0, 0)

    #     # to CONTAIN the label elements
    #     self.container = QWidget()
    #     self.container.setStyleSheet(
    #         '''
    #         background: white;
    #         '''
    #     )

    #     # self.label = QLabel(self.container)
    #     # self.label.setText("first label")

    #     # adding DROP SHADOW to the CONTAINER
    #     effect = QGraphicsDropShadowEffect()
    #     effect.setBlurRadius(5);
    #     effect.setXOffset(0)
    #     effect.setYOffset(0)
    #     self.container.setGraphicsEffect(effect)

    #     # LEFT and RIGHT SPACER
    #     verticalSpacer = QtWidgets.QSpacerItem(
    #         80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

    #     # ADDING CONTAINER to HORIZONTAL BOX
    #     hbox.addItem(verticalSpacer)
    #     hbox.addWidget(self.container)
    #     hbox.addItem(verticalSpacer)

    #     self.vbox_layout.addLayout(hbox)
