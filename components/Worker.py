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
    progress = pyqtSignal(list)

    def thread_function_init(self, img,page_width,page_height,zoom):
        self.img = img
        self.page_width = page_width
        self.page_height = page_height
        self.zoom = zoom
 

    def thread_function(self):
        """Long-running task."""
        cvImage = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
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

        # img_bytes = self.img.tobytes()

        # qim = QImage(img_bytes, self.img.size[0],
        #              self.img.size[1], QImage.Format_RGB888)
        cv2.imwrite('cfile.png',np.array(self.img))
        pixMap = QPixmap.fromImage(QImage('cfile.png'))
        # pixMap = QPixmap(qim)

        pixMap = pixMap.scaled(self.page_width,
                               self.page_height*self.zoom, Qt.KeepAspectRatio)
        
        pixMap_width = pixMap.size().width()
        pixMap_height = pixMap.size().height()

        # label creation per line

        img_height = self.img.height
        img_width = self.img.width
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

        self.finished.emit()
        self.progress.emit([no_of_lines,pixMap,bounding_box,height_ratio,width_ratio])   
        # return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]
        