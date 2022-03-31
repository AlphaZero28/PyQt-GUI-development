from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel, QPushButton, QTextEdit
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QImage,QFont
from fitz.fitz import PDF_SIGNATURE_ERROR_DIGEST_FAILURE, Pixmap
from components.ToolBar import cToolBar
from components.ImageProcessing import imgProcess
from components.config import debug
import PIL.Image as Image
import io
import numpy as np
import cv2
# from PySide2.QtGui import QAccessible, QAccessibleEvent, QAccessibleInterface
# from PySide2.QtCore import QObject
# import PySide2.QtWidgets as pyQtWidget

from components.ImageProcessing import imgProcess
# import matplotlib.pyplot as plt
from components.Worker import Worker

from PyQt5.QtCore import QObject, QThread, pyqtSignal

class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout
        self.mainwindow = mainwindow
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.imgs = []
        self.zoom = 1.75
        self.page_num = 0
        self.run_count = 0

        self.vbox_layout.addWidget(self.scroll_area, 10)


        # LEFT and RIGHT SPACER
        self.verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        if debug:
            self.debug_show_page()

        

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

    def set_path(self,path):
        self.path = path
        self.page_num = 0
        self.goto_page(self.page_num)

    def goto_specific_page(self, page_number):
        # print(page_num)
        if page_number>=0 and page_number < len(self.imgs):
            self.goto_page(page_number)

    def goto_next_page(self):
        if not self.page_num == len(self.imgs)-1:
            self.page_num = self.page_num+1
            self.goto_page(self.page_num)

    def goto_prev_page(self):
        if not self.page_num == 0:
            self.page_num = self.page_num-1
            self.goto_page(self.page_num)

    def goto_page(self, page_num):
        # self.mainwindow.cstatus_bar.show_msg('working')
        img = imgProcess.get_single_page(self.path,page_num)

        # Step 2: Create a QThread object
        # self.thread = QThread()
        # # Step 3: Create a worker object
        # self.worker = Worker()
        # self.worker.init(self,self.vbox_layout,self.scroll_area,self.verticalSpacer,img, self.zoom, self.page_num)
        # # Step 4: Move worker to the thread
        # self.worker.moveToThread(self.thread)
        # # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # # self.worker.progress.connect(self.reportProgress)
        # # Step 6: Start the thread
        # self.thread.start()

        self.show_single_page(img)
        # self.show_single_page(self.imgs[page_num])

    
    def debug_show_page(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        groupBox = QGroupBox()  # groupBox will contain the formLayout of the pages
        form_layout = QFormLayout()

        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(0)

        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setStyleSheet('background: white;')

        line2 = QPushButton('১৮২০ সালে জন্মগ্রহণ করেন ',container)
        line2.setFont(QFont('Arial',12))
        line2.setDefault(False)
        line2.adjustSize()
        line2.move(100,200)
        line2.setFlat(True)
        # line2.setAccessibleName('butt')
        line2.setAccessibleDescription('১৮২০ সালে জন্মগ্রহণ করেন ')
        line2.setFocus()

        line3 = QPushButton('১৮২০ সালে জন্মগ্রহণ করেন ',container)
        line3.setFont(QFont('Arial',12))
        line3.adjustSize()
        line3.move(100,300)
        line3.setFlat(True)

        line = QLabel(container)
        line.setText('১৮২০ সালে জন্মগ্রহণ করেন 2')
        line.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # line.setTextInteractionFlags(Qt.TextSelectableByMouse)
        line.setStyleSheet("background:white")
        # QWidget.setTabOrder(line,line3)
        line.setFont(QFont('Arial',12))
        # line.setAccessibleDescription('১৮২০ সালে জন্মগ্রহণ করেন ')
        line.adjustSize()
        # print(i)
        line.move(100,400)
        

        
        # line.adjustSize()

        # line3.setDefault(False)
        # line3.setAutoDefault(False)

        # line4 = QTextEdit(container)
        # line4.setReadOnly(True)
        # line4.setText('১৮২০ সালে জন্মগ্রহণ করেন \n বাংলাদেশ এর সকল ব্লগ এর লিস্ট একবার দেখে নিন')
        # line4.setFont(QFont('Arial',12))
        # line4.setStyleSheet("border: 0px solid black; ")
        # line4.adjustSize()
        # line4.move(100,500)

        
        hbox_temp.addItem(self.verticalSpacer)
        hbox_temp.addWidget(container)
        hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget(self)

        tempQW.setLayout(hbox_temp)

        form_layout.addRow(tempQW)
        groupBox.setLayout(form_layout)

        scroll_area.setWidget(groupBox)

        self.vbox_layout.replaceWidget(self.scroll_area, scroll_area)
        self.scroll_area = scroll_area
        # self.scroll_area.setFocus()

        # self.debug_accessibility()
        
    # def save_file(self):
    #     [tempQW, page_text] = self.create_page(self.imgs[0])
    #     print(page_text)
    def debug_accessibility(self):
        pass
        # print('accessibility debug', QAccessible.isActive())
        # qobj = QObject()
        # qobj = pyQtWidget.QLabel()
        # qobj.setText('hello')
        # event = QAccessibleEvent(qobj, QAccessible.Focus)
        # QAccessible.updateAccessibility(event)

    def show_single_page(self, img):

        self.run_count = self.run_count+1

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        groupBox = QGroupBox()  # groupBox will contain the formLayout of the pages
        form_layout = QFormLayout()

        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(0)

        no_page = len(self.imgs)

        [tempQW] = self.create_page(img)
        form_layout.addRow(tempQW)
        groupBox.setLayout(form_layout)


        scroll_area.setWidget(groupBox)


        self.vbox_layout.replaceWidget(self.scroll_area, scroll_area)
        self.scroll_area = scroll_area
        self.scroll_area.setAccessibleName('Page Number '+str(self.page_num+1))
        self.scroll_area.setFocus()

        self.debug_accessibility()
        

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

        # DROP SHADOW EFFECT
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setXOffset(0)
        effect.setYOffset(0)

        container.setGraphicsEffect(effect)
        label = QLabel(container)
        label.setText("first label")
       
        [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio] = self.process(img,page_width,page_height)

        pixMap_width = pixMap.size().width()
        pixMap_height = pixMap.size().height()

        container.setFixedWidth(pixMap_width)
        container.setFixedHeight(pixMap_height)

        label.setPixmap(pixMap)

        # label creation per line

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        hbox_temp = QHBoxLayout()
        hbox_temp.setContentsMargins(0, 0, 0, 0)

        if no_of_lines == 0:            
            hbox_temp.addItem(self.verticalSpacer)
            hbox_temp.addWidget(container)
            hbox_temp.addItem(self.verticalSpacer)

        else:
            bounding_vertical_rect = []
            
            
            for i, (x1, x2, r1, r2, txt) in enumerate(bounding_box):                
            
                line = QLabel(container)
                
                line.setText(txt)
                line.setTextInteractionFlags(Qt.TextSelectableByMouse)
                line.setStyleSheet("background:white")
                
                line.setFont(QFont('Arial',12))
                line.adjustSize()
                # print(i)
                line.move(x1*width_ratio, r1*height_ratio)
                line.adjustSize()
                line.setFixedHeight((r2-r1+12)*height_ratio)
                line.setFixedWidth((x2-x1+150)*width_ratio)
                line.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

                
            hbox_temp.addItem(self.verticalSpacer)
            hbox_temp.addWidget(container)

            hbox_temp.addItem(self.verticalSpacer)

        tempQW = QWidget()

        tempQW.setLayout(hbox_temp)

        return [tempQW]

    def process(self,img,page_width,page_height):       
        cvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # convert to gray img
        gray_img = imgProcess.bgr2gray(cvImage)
        # convert to invert image
        inv_img = imgProcess.invertImage(gray_img)
        # convert to horizontal histogram
        [hist_img, hist_data] = imgProcess.horizontal_hist(inv_img)
        # get horizontal rounding_rect
        bounding_horizontal_rect = imgProcess.bounding_horizontal_rect(
            hist_data)

        no_of_lines = len(bounding_horizontal_rect)
        # print(bounding_horizontal_rect)

        # cropped img
        lines = imgProcess.find_lines(bounding_horizontal_rect, inv_img)

        img_bytes = img.tobytes()

        qim = QImage(img_bytes, img.size[0],
                     img.size[1], QImage.Format_RGB888)
        # pixMap = QPixmap.fromImage(img)
        pixMap = QPixmap(qim)

        pixMap = pixMap.scaled(page_width,
                               page_height*self.zoom, Qt.KeepAspectRatio)
        
        pixMap_width = pixMap.size().width()
        pixMap_height = pixMap.size().height()

        # label creation per line

        img_height = img.height
        img_width = img.width
        height_ratio = pixMap_height/img_height
        width_ratio = pixMap_width/img_width

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        page_text = []
        bounding_box = []
        if no_of_lines == 0:            
            return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]
        else:
            bounding_vertical_rect = []
            
            
            for i, (r1, r2) in enumerate(bounding_horizontal_rect):                
            # ocr applied on each line 

                [vert_img, vert_data] = imgProcess.vertical_hist(lines[i])
                # line_vert_hist_data.append(vert_data)

            # find bounding_verting_rect
                words_in_line = imgProcess.bounding_vertical_rect(vert_data)

                initial = words_in_line[0][0]
                final = words_in_line[-1][1]

                image = lines[i][:,initial:final]

                # print(initial, final)
                # print(words_in_line)
                
                bounding_vertical_rect.append(words_in_line)
                # print(bounding_vertical_rect)
                txt = imgProcess.pytesseract_apply(image,flag=0, line=i)

                # print(txt)
                if len(txt) == 0 :
                    txt = imgProcess.pytesseract_apply(lines[i],flag=1, line=i)
                page_text.append(txt)

                x1 = bounding_vertical_rect[i][0][0]
                x2 = bounding_vertical_rect[i][-1][1]
                
                bounding_box.append((x1,x2,r1,r2,txt))
                
        return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]