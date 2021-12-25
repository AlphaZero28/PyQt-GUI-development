from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QImage


class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.mainwindow = mainwindow

        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # self.set_scrollview()

    def set_scrollview(self, imgs):
        # creating a HORIZONTAL LAYOUT to add to the vertical layout
        # hbox = QHBoxLayout()
        # hbox.setContentsMargins(0, 0, 0, 0)

        # main SCROLL AREA
        self.scroll_area = QScrollArea()

        # FORM LAYOUT will contain the labels
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(10)

        no_page = len(imgs)
        print(imgs[0].width())

        # adding the PAGES as labels to form_layout
        for i in range(1):
            print('test')
            page_width = imgs[i].width()
            page_height = imgs[i].height()
            print(page_height, page_width)
            tempQW = self.create_page(imgs[i])

            # tempQW = self.img_show(imgs[i], page_height, page_width)
            # tempQW = QWidget()
            form_layout.addRow(tempQW)

        groupBox = QGroupBox()
        groupBox.setLayout(form_layout)

        self.scroll_area.setWidget(groupBox)
        self.scroll_area.setWidgetResizable(True)

        # hbox.addWidget(self.scroll_area)

        # self.vbox_layout.addLayout(hbox)
        self.vbox_layout.addWidget(self.scroll_area, 10)

    # def img_show(self, img, page_height, page_width):
    #     # print(img, page_height, page_width)
    #     container = QWidget()
    #     container.setStyleSheet('background: white;')

    #     self.label = QLabel()
    #     txt = " lable loaded" + str(page_width) + str(page_width) + "dim"
    #     self.label.setText(txt)

    def create_page(self, qtimg):
        container = QWidget()
        container.setStyleSheet('background: white;')
        page_width = QtWidgets.QDesktopWidget().screenGeometry().width()-3*80
        # self.page_height = 50
        page_height = 100
        container.setFixedWidth(page_width)
        # container.setFixedWidth(self.scroll_area.size().width()-2*80)
        container.setFixedHeight(page_height)
        # container.adjustSize()
        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setXOffset(0)
        effect.setYOffset(0)

        container.setGraphicsEffect(effect)
        label = QLabel(container)
        label.setText("first label")
        label.setStyleSheet('border: 3px solid gray')
        label.setGeometry(QRect(0, 0, page_width, page_height))

        # adding pixmap
        pixMap = QPixmap.fromImage(qtimg)
        label.setPixmap(pixMap)
        # label.adjustSize()

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
