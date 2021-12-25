import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QBoxLayout, QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget
import fitz
from PIL import Image
from PIL.ImageQt import ImageQt
# from pdf2image import convert_from_path

def get_pages(filename):
    # images = convert_from_path(filename)
    # print(images[0])
    doc = fitz.open(filename)
    no_page = len(doc)
    imgs = []

    temp_filename = 'temp.png'
    for i in range(no_page):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        # fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        # qtimg = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
        # imgs.append(qtimg)
        # pix.pil_save(temp_filename)
        # img = Image.open(temp_filename)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        imgs.append(img)
        
    return imgs 

    
def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)

    vbox = QVBoxLayout(w)

    images = get_pages('Jhora Palok By Jibanananda Das (BDeBooks.Com).pdf')
    
    
    label = QtWidgets.QLabel()
    label.setGeometry(QRect(0,0,100,100))
    label.setText("Hello")
    # qtimg = QImage("./assets/ocean.jpg")
    qim = ImageQt(images[0])
    pix = QPixmap.fromImage(qim)
    label.setPixmap(pix)
    label.adjustSize()

    vbox.addWidget(label)

    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()