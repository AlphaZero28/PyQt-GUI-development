'''Load thread processes (load file and process)'''
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel, QPushButton, QTextEdit
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QImage,QFont
from fitz.fitz import PDF_SIGNATURE_ERROR_DIGEST_FAILURE, Pixmap
# from matplotlib.pyplot import text
from components.ImageProcessing import imgProcess
from components.config import DEBUG
import PIL.Image as Image
import io
import numpy as np
import cv2


def ocr_on_page(img):
        """Long-running task."""
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

        # CREATING a HORIZONTAL LAYOUT to contain spacers and the container
        page_text = []
        bounding_box = []
        if no_of_lines == 0:            
            return [no_of_lines,bounding_box]
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

        # self.finished.emit()
        # self.progress.emit([no_of_lines,pixMap,bounding_box,height_ratio,width_ratio])   
        return [no_of_lines,bounding_box]


def ocr_load_pages(current_path, total_page_number):
    page_text = []
    for pi in range(total_page_number):
        page_text.append([])
        img = imgProcess.get_single_page(current_path,pi)
        [no_of_lines,bounding_box] = ocr_on_page(img)
        for i, (x1, x2, r1, r2, txt) in enumerate(bounding_box): 
            page_text[pi].append(txt)
  
    return page_text

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)

    def thread_function_init(self, img):
        self.img = img
 

    def thread_function(self):
        # """Long-running task."""
        lst = ocr_on_page(self.img)
        self.finished.emit()
        self.progress.emit(lst)   
        # return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]


class SaveFileWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)


    def thread_function_init(self, current_path, total_page_number ,save_filename):
        self.current_path = current_path
        self.save_filename = save_filename
        self.total_page_number = total_page_number
 

    def thread_function(self):
        """Long-running task."""

        page_text = ocr_load_pages(self.current_path, self.total_page_number)
        self.finished.emit()
        self.progress.emit(page_text)   
        # return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]