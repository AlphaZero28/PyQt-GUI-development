import cv2
import numpy as np
import io
import PIL.Image as Image
import fitz
import pytesseract

# import matplotlib.pyplot as plt
import platform

if platform.system().lower()=='windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class imgProcess():

    def pdf2img(filename):
        '''' convert pdf pages into PNG image file'''

        doc = fitz.open(filename)
        no_page = len(doc)
        imgs = []
        zoom = 4   # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        for i in range(no_page):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            pix.set_dpi(5000, 7200)
            # img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_data = pix.tobytes()  # pix data to bytes
            # convert to an pillow image
            img = Image.open(io.BytesIO(img_data))
            opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            imgs.append(opencvImage)

        return imgs

    def get_pages(filename):
        ''' returns the pages from the given pdf file'''
        # images = convert_from_path(filename)
        # print(images[0])
        doc = fitz.open(filename)
        no_page = len(doc)
        imgs = []
        zoom = 4   # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        for i in range(no_page):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            pix.set_dpi(5000, 7200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            imgs.append(img)

        return imgs

    def bgr2gray(img):
        ''' convert to gray image '''
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def invertImage(img):
        ''' invert pixels if 255 is dominant'''

        if (img.sum(axis=1).sum()/img.size) > 50:
            # img = 255- img
            ret, img = cv2.threshold(
                img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return img

    def horizontal_hist(img):
        ''' calculahorizontal histogram of the image '''

        projection = np.sum(img, 1) / 255
        result = np.zeros((projection.shape[0], img.shape[1]))
        for row in range(img.shape[0]):
            # /max(projection)*img.shape[1]
            x2 = int(projection[row])
            cv2.line(result, (0, row), (x2, row), (255, 255, 255), 1)

        return [result, projection]

    def bounding_horizontal_rect(hist_data):
        ''' returns the initial and final y axis point of each line'''
        bounding_horizontal_rect = []
        valp, pos1, thresh_val = 0,0,0


        for i, val in enumerate(hist_data):
            if val > thresh_val and valp <= thresh_val:
                pos1 = i-1

            elif (not i == 0) and val <= thresh_val and valp > thresh_val:
                if (i-pos1) > 2:
                    bounding_horizontal_rect.append((pos1, i+1))
            valp = val

        return bounding_horizontal_rect



    def find_lines(bounding_horizontal_rect, img):
        ''' Find lines that exist in the image'''

        cropped_images = []
        for i, (r1, r2) in enumerate(bounding_horizontal_rect):
            crop_img = img[r1:r2, 0:img.shape[1]]
            cropped_images.append(crop_img)

        return cropped_images

    def vertical_hist(img):
        ''' meant to be used after horizontal histogram in each line'''
        projection = np.sum(img, 0) / 255
        result = np.zeros((img.shape[0], projection.shape[0]))

        for col in range(img.shape[1]):
            x2 = int(projection[col])
            cv2.line(result, (col, 0), (col, x2), (255, 255, 255), 1)

        return [result, projection]

    def bounding_vertical_rect(vert_data):
        ''' returns the initial and final x axis point of each word'''
        
        bounding_vertical_rect = []
        valp, pos1, thresh_val = 0,0,0

        for i, val in enumerate(vert_data):
            if val > thresh_val and valp <= thresh_val:
                pos1 = i-1

            elif (not i == 0) and val <= thresh_val and valp > thresh_val:
                if (i-pos1) > 2:
                    bounding_vertical_rect.append((pos1, i+1))
            valp = val

        return bounding_vertical_rect

    def find_words( bounding_vertical_rect, img):
        ''' Find words in the line image'''
        cropped_images = []
        for i, (r1, r2) in enumerate(bounding_vertical_rect):
            crop_img = img[0:img.shape[1], r1:r2]
            cropped_images.append(crop_img)

        return cropped_images

    def pytesseract_apply( img, flag, line = 0):
        ''' Text detection in the image. 
        flag = 0 when image conatains line text. 
        flag = 1 when image containes word text '''


        if flag == 0:
            set_config = '--psm 7'
        elif flag == 1:
            set_config = '--psm 3'
        # im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        im2 = np.pad(img, ((10, 10), (100, 100)), 'constant',
                     constant_values=(0, 0))

        # if line == 5:
        #     plt.imshow(im2, cmap='gray')
        #     plt.show()
        #     plt.axis('off')

        text = pytesseract.image_to_string(
            im2, lang='ben', config=set_config)
        return text
