from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QImage
from fitz.fitz import Pixmap


class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.mainwindow = mainwindow

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.groupBox = QGroupBox() # groupBox will contain the formLayout of the pages

        self.scroll_area.setWidget(self.groupBox)

        self.vbox_layout.addWidget(self.scroll_area, 10)

        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # self.set_scrollview()

    # def set_single_view(self, img):
    #     self.tempQW = self.create_page(img)
    #     self.vbox_layout.addWidget(self.tempQW, 10)
    #     print(self.tempQW.height())

    def set_scrollview(self, imgs):
        # FORM LAYOUT will contain the labels
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(10)

        no_page = len(imgs)


        # adding the PAGES as labels to form_layout
        for i in range(no_page):
            tempQW = self.create_page(imgs[i])
            form_layout.addRow(tempQW)

        self.groupBox.setLayout(form_layout)
        print('scroll height:',self.scroll_area.height())

    def create_page(self, img):
        container = QWidget()
        container.setStyleSheet('background: white;')
        page_width = QtWidgets.QDesktopWidget().screenGeometry().width()-3*80
        page_height = self.scroll_area.height()
        # page_height =  QtWidgets.QDesktopWidget().screenGeometry().height()
        container.setFixedWidth(page_width)
        container.setFixedHeight(page_height)
        
        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setXOffset(0)
        effect.setYOffset(0)

        container.setGraphicsEffect(effect)
        label = QLabel(container)
        label.setText("first label")
        # label.setStyleSheet('border: 3px solid gray')
        label.setGeometry(QRect(0, 0, page_width, page_height))

        # adding pixmap
        img = img.convert("RGB")
        data = img.tobytes("raw","RGB")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
        # pixMap = QPixmap.fromImage(img)
        pixMap = QPixmap(qim)
        
        # label.setPixmap(pixMap)
        pixMap = pixMap.scaled(page_width,page_height,Qt.KeepAspectRatio)
        container.setFixedWidth(pixMap.size().width())
        label.setPixmap(pixMap)
        # label.adjustSize()
        # container.adjustSize()

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0, 0, 0, 0)
        hbox_temp.addItem(self.verticalSpacer)
        hbox_temp.addWidget(container)
        hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget()
        tempQW.setLayout(hbox_temp)

        return tempQW

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