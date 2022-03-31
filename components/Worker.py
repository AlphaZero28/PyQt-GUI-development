'''Load thread processes (load file and process)'''
from PyQt5.QtCore import QObject, QThread, pyqtSignal
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


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def init(self, mainview, vbox_layout, scroll_area, verticalSpacer, img, zoom, page_num):
        self.mainview = mainview
        self.vbox_layout = vbox_layout
        self.scroll_area = scroll_area
        self.verticalSpacer = verticalSpacer
        self.img = img
        self.zoom = zoom
        self.page_num = page_num


    def run(self):
        """Long-running task."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        groupBox = QGroupBox()  # groupBox will contain the formLayout of the pages
        form_layout = QFormLayout()

        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(0)

        [tempQW, pg_text] = self.create_page(self.img)
        form_layout.addRow(tempQW)
        groupBox.setLayout(form_layout)


        scroll_area.setWidget(groupBox)


        self.vbox_layout.replaceWidget(self.scroll_area, scroll_area)
        self.scroll_area = scroll_area
        self.scroll_area.setAccessibleName('Page Number '+str(self.page_num+1))
        self.scroll_area.setFocus()
        # for i in range(5):
        #     self.progress.emit(i + 1)
        self.finished.emit()
    
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
        gray_img = imgProcess.bgr2gray(cvImage)

        # plt.imshow(gray_img, cmap='gray')

        # convert to invert image
        inv_img = imgProcess.invertImage(gray_img)
        # plt.imshow(inv_img)

        # convert to horizontal histogram
        [hist_img, hist_data] = imgProcess.horizontal_hist(inv_img)

        # plt.imshow(hist_img)

        # get horizontal rounding_rect
        bounding_horizontal_rect = imgProcess.bounding_horizontal_rect(
            hist_data)

        no_of_lines = len(bounding_horizontal_rect)
        # print(bounding_horizontal_rect)

        # cropped img
        lines = imgProcess.find_lines(bounding_horizontal_rect, inv_img)

        # plt.imshow(lines[0],cmap='gray')
        # plt.imshow(lines[1],cmap='gray')
        # plt.show()
        cv2.imwrite('line-1.png', lines[0])
        cv2.imwrite('line-2.png', lines[1])
        # print(len(lines))


        # vertical histogram applied on each line
        # line_vert_hist_data = []
        # bounding_vertical_rect = []
        # for i in range(no_of_lines):

        #     [vert_img, vert_data] = imgProcess.vertical_hist(lines[i])
        #     # line_vert_hist_data.append(vert_data)

        # # find bounding_verting_rect
        #     words_in_line = imgProcess.bounding_vertical_rect(vert_data)
        #     bounding_vertical_rect.append(words_in_line)


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
        page_text = []

        if no_of_lines == 0:            
            hbox_temp.addItem(self.verticalSpacer)
            hbox_temp.addWidget(container)
            hbox_temp.addItem(self.verticalSpacer)

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
                    # print(i+1)
                    # words = imgProcess.find_words(words_in_line,
                    #                             lines[i])
                    # for word in words :
                    #     # plt.axis('off')
                    #     # plt.imshow(word, cmap='gray')
                    #     # plt.figure(i+1)
                    #     word_found = imgProcess.pytesseract_apply(lines[i],flag=1 )
                        # txt += str(word_found + " ")


                # save txt to txt file 
                # with open('sample.txt', 'a') as f:
                #     if not i==1: f.write('\n')
                #     f.write(txt)
                page_text.append(txt)

                x1 = bounding_vertical_rect[i][0][0]
                x2 = bounding_vertical_rect[i][-1][1]
                
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

        return [tempQW, page_text]