import cv2
import numpy as np
import io
import PIL.Image as Image
import fitz
from torchvision import transforms


class imgProcess():

    def pdf2img(self, filename):
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

    def get_pages(self, filename):
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

    def bgr2gray(self, img):
        ''' convert to gray image '''
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def invertImage(self, img):
        ''' invert pixels if 255 is dominant'''

        if (img.sum(axis=1).sum()/img.size) > 50:
            # img = 255- img
            ret, img = cv2.threshold(
                img, 0, 255, cv2.THRESH_BINARY_INV)

        return img

    def horizontal_hist(self, img):
        ''' calculahorizontal histogram of the image '''

        projection = np.sum(img, 1) / 255
        result = np.zeros((projection.shape[0], img.shape[1]))
        for row in range(img.shape[0]):
            # /max(projection)*img.shape[1]
            x2 = int(projection[row])
            cv2.line(result, (0, row), (x2, row), (255, 255, 255), 1)

        return [result, projection]

    def bounding_horizontal_rect(self, hist_data):
        ''' returns the initial and final y axis point of each line'''
        bounding_horizontal_rect = []
        valp = 0
        pos1 = 0
        thresh_val = 0

        for i, val in enumerate(hist_data):
            if val > thresh_val and valp <= thresh_val:
                pos1 = i-1

            elif (not i == 0) and val <= thresh_val and valp > thresh_val:
                if (i-pos1) > 2:
                    bounding_horizontal_rect.append((pos1, i+1))
            valp = val

        return bounding_horizontal_rect

    def find_lines(self, bounding_horizontal_rect, img):
        cropped_images = []
        for i, (r1, r2) in enumerate(bounding_horizontal_rect):
            crop_img = img[r1:r2, 0:img.shape[1]]
            cropped_images.append(crop_img)

        return cropped_images

    def vertical_hist(self, img):
        ''' meant to be used after horizontal histogram in each line'''
        projection = np.sum(img, 0) / 255
        result = np.zeros((img.shape[0], projection.shape[0]))

        for col in range(img.shape[1]):
            x2 = int(projection[col])
            cv2.line(result, (col, 0), (col, x2), (255, 255, 255), 1)

        return [result, projection]

    def bounding_vertical_rect(self, vert_data):
        bounding_vertical_rect = []
        valp = 0
        pos1 = 0
        thresh_val = 0

        for i, val in enumerate(vert_data):
            if val > thresh_val and valp <= thresh_val:
                pos1 = i-1

            elif (not i == 0) and val <= thresh_val and valp > thresh_val:
                if (i-pos1) > 2:
                    bounding_vertical_rect.append((pos1, i+1))
            valp = val

        return bounding_vertical_rect

    def sliding_img_resize(self, image):
        ''' resize the sliding window img as per aspect ratio of the original img'''
        col_num, row_num = 16, 28
        aspect_ratio = col_num/row_num
        image = transforms.ToPILImage()(image)
        image = transforms.Resize((row_num, col_num))(image)
        ret, image = cv2.threshold(
            np.array(image), 150, 255, cv2.THRESH_BINARY)

        return image

    def sliding_window(self, lines):
        slide_imgs = []
        ran_interval = 6
        aspect_ratio = 16/28
        ran = np.arange(0, lines.shape[1], ran_interval)

        for i in ran:
            c1, c2 = i, i+int(aspect_ratio*lines.shape[0])
            gap = lines[:, c1:c2]
            gap = self.sliding_img_resize(gap)
            slide_imgs.append(gap)
            # print(type(slide_imgs))

        return slide_imgs
