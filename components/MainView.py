from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui

class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.mainwindow = mainwindow

        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.set_scrollview()

    def set_scrollview(self):
        # creating a HORIZONTAL LAYOUT to add to the vertical layout
        # hbox = QHBoxLayout()
        # hbox.setContentsMargins(0, 0, 0, 0)

        # main SCROLL AREA
        self.scroll_area = QScrollArea()

        



        # FORM LAYOUT will contain the labels
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0,0,0,0)
        form_layout.setVerticalSpacing(10)

        # adding the PAGES as labels to form_layout
        for i in range(20):
            tempQW = self.create_page()

            form_layout.addRow(tempQW)

        
        groupBox = QGroupBox()
        groupBox.setLayout(form_layout)
  
        self.scroll_area.setWidget(groupBox)
        self.scroll_area.setWidgetResizable(True)

        # hbox.addWidget(self.scroll_area)

        # self.vbox_layout.addLayout(hbox)
        self.vbox_layout.addWidget(self.scroll_area,10)

    def create_page(self):
        container = QWidget()

        container.setStyleSheet('background: white;')
        page_width = QtWidgets.QDesktopWidget().screenGeometry().width()-3*80
        page_height = 100
        container.setFixedWidth(page_width)
        # container.setFixedWidth(self.scroll_area.size().width()-2*80)
        container.setFixedHeight(page_height)
        # container.adjustSize()
        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5);
        effect.setXOffset(0)
        effect.setYOffset(0)

        container.setGraphicsEffect(effect)
        label = QLabel(container)
        label.setText("first label")
        label.setStyleSheet('border: 3px solid gray')
        label.setGeometry(QRect(0,0,page_width, page_height))
        

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0,0,0,0)
        hbox_temp.addItem(self.verticalSpacer)
        hbox_temp.addWidget(container)
        hbox_temp.addItem(self.verticalSpacer)
        

        tempQW = QWidget()
        tempQW.setLayout(hbox_temp)

        return tempQW


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



        
        