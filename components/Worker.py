'''Load thread processes (load file and process)'''
from cProfile import run
import io
import os
from traceback import print_tb
import time
import cv2
import numpy as np
import PIL.Image as Image
from fitz.fitz import PDF_SIGNATURE_ERROR_DIGEST_FAILURE, Pixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QRect, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (QFormLayout, QGraphicsDropShadowEffect, QGroupBox,
                             QHBoxLayout, QLabel, QMessageBox, QProgressBar,
                             QPushButton, QScrollArea, QTextEdit, QVBoxLayout,
                             QWidget)

from components.config import DEBUG
# from matplotlib.pyplot import text
from components.ImageProcessing import imgProcess
import logging

logging.basicConfig(level=logging.INFO, filename='pathok.log', filemode='w',
                    format="%(levelname)s - %(message)s")

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

        logging.info("image preprocessing done")
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

# running_page = 0
# def ocr_load_pages(current_path, total_page_number):
#     page_text = []
#     for pi in range(total_page_number):
#         page_text.append([])
#         img = imgProcess.get_single_page(current_path,pi)
#         [no_of_lines,bounding_box] = ocr_on_page(img)
#         for i, (x1, x2, r1, r2, txt) in enumerate(bounding_box): 
#             page_text[pi].append(txt)
  
#     return page_text

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)
    
    # logging starting
    logging.info("Pathok Starts")
    logging.info("Threading starts")

    def thread_function_init(self, img):
        self.img = img


    def thread_function(self):
        # """Long-running task."""
        tessdata_ben = r"C:\Program Files\Tesseract-OCR\tessdata\ben.traineddata"
        tesseract_dir = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        if os.path.exists(tessdata_ben) ==True:
            logging.info("bangla tessdata found!")
        else:
            logging.error("bangla tessdata not found!")

        if os.path.exists(tesseract_dir):
            logging.info("Tesseract found!")
        else:
            logging.info("Tesseract not found! Install tesseract")

        lst = ocr_on_page(self.img)
        self.finished.emit()
        self.progress.emit(lst)   
        # return [no_of_lines,pixMap,bounding_box,height_ratio,width_ratio]


class SaveFileWorker(QObject):
    finished = pyqtSignal()
    settext = pyqtSignal(list)
    progress = pyqtSignal(int)
    # pyqt signal for saving progress

    


    def thread_function_init(self, current_path, total_page_number ,save_filename):
        self.current_path = current_path
        self.save_filename = save_filename
        self.total_page_number = total_page_number

    def thread_function(self):
        """Long-running task."""
        # print('saving started')
        page_text = []
        for pi in range(self.total_page_number):
            page_text.append([])
            img = imgProcess.get_single_page(self.current_path,pi)
            [no_of_lines,bounding_box] = ocr_on_page(img)
            for i, (x1, x2, r1, r2, txt) in enumerate(bounding_box): 
                page_text[pi].append(txt)
            self.progress.emit(pi+1)
        self.settext.emit(page_text)
        self.finished.emit()