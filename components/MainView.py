from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QImage
from fitz.fitz import PDF_SIGNATURE_ERROR_DIGEST_FAILURE, Pixmap
from components.ToolBar import cToolBar
from components.ImageProcessing import imgProcess
import PIL.Image as Image
import io
import numpy as np
import cv2
import matplotlib.pyplot as plt


class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.imgProcess = imgProcess()
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
        if not self.page_num == len(self.imgs)-1:
            self.page_num = self.page_num+1
            self.goto_page(self.page_num)

    def goto_prev_page(self):
        if not self.page_num == 0:
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
        # img = img.convert("RGB")
        # data = img.tobytes("raw", "RGB")

        # convert to PIL img
        # image = Image.open(io.BytesIO(img_data))

        # convert to cv2 img
        cvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # convert to gray img
        gray_img = self.imgProcess.bgr2gray(cvImage)

        # convert to invert image
        inv_img = self.imgProcess.invertImage(gray_img)

        # convert to horizontal histogram
        [hist_img, hist_data] = self.imgProcess.horizontal_hist(inv_img)

        # get horizontal rounding_rect
        bounding_horizontal_rect = self.imgProcess.bounding_horizontal_rect(
            hist_data)

        no_of_lines = len(bounding_horizontal_rect)
        # print(bounding_horizontal_rect)

        #  get cropped imgs of line in each page
        lines = self.imgProcess.find_lines(bounding_horizontal_rect, inv_img)

        # for im in lines:
        #     plt.imshow(im, cmap='gray')
        #     plt.show()

        # vertical histogram applied on each line
        line_vert_hist_data = []
        for i in range(no_of_lines):

            [vert_img, vert_data] = self.imgProcess.vertical_hist(lines[i])
            line_vert_hist_data.append(vert_data)

        # find bounding_verting_rect
        bounding_vertical_rect = []
        for i in range(len(line_vert_hist_data)):
            words_in_line = self.imgProcess.bounding_vertical_rect(
                line_vert_hist_data[i])
            bounding_vertical_rect.append(words_in_line)

        # print(word_data)

        # hist_img_rgb = cv2.cvtColor(hist_img, cv2.COLOR_GRAY2RGB)

        img_bytes = img.tobytes()

        qim = QImage(img_bytes, img.size[0],
                     img.size[1], QImage.Format_RGB888)
        # pixMap = QPixmap.fromImage(img)
        pixMap = QPixmap(qim)

        pixMap = pixMap.scaled(page_width,
                               page_height*self.zoom, Qt.KeepAspectRatio)
        label.setGeometry(QRect(0, 0, pixMap.width(), pixMap.height()))

        self.pixMap_width = pixMap.size().width()
        self.pixMap_height = pixMap.size().height()

        container.setFixedWidth(self.pixMap_width)
        container.setFixedHeight(self.pixMap_height)

        label.setPixmap(pixMap)

        # label creation per line

        img_height = img.height
        img_width = img.width
        height_ratio = self.pixMap_height/img_height
        width_ratio = self.pixMap_width/img_width

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0, 0, 0, 0)

        if no_of_lines == 0:
            hbox_temp.addItem(self.verticalSpacer)
            hbox_temp.addWidget(container)
            hbox_temp.addItem(self.verticalSpacer)

        else:

            # sliding window
            slide_imgs = self.imgProcess.sliding_window(lines[1])

            # print(type(slide_imgs))
            # save sliding windows

            for i, s_img in enumerate(slide_imgs):
                dir_name = 'D:\pyqt\hist\slide-img\img' + str(i) + '.png'
                cv2.imwrite(dir_name, s_img)

            for i, (r1, r2) in enumerate(bounding_horizontal_rect):

                x1 = bounding_vertical_rect[i][0][0]
                x2 = bounding_vertical_rect[i][-1][1]
                line = QLabel(container)
                line.setStyleSheet("background:rgba(0,255,0,100);")
                line.setText("line" + str(i))
                # print(i)
                line.move(x1*width_ratio, r1*height_ratio)
                # line.adjustSize()
                line.setFixedHeight((r2-r1+10)*height_ratio)
                line.setFixedWidth((x2-x1+10)*width_ratio)

            hbox_temp.addItem(self.verticalSpacer)
            hbox_temp.addWidget(container)

            hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget(self)

        tempQW.setLayout(hbox_temp)

        return tempQW
