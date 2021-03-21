#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import os
import re
import cv2
from PIL import Image


class pdf:

    def __init__(self):
        super().__init__()
        self.alpha_slider_max = 100

    def mark_region(self, image_path):

        im = cv2.UMat(cv2.imread(image_path))

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            30,
            )

                # Dilate to combine adjacent text contours

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilate = cv2.dilate(thresh, kernel, iterations=4)

                # Find contours, highlight text areas, and extract ROIs

        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = (cnts[0] if len(cnts) == 2 else cnts[1])
        image = None
        line_items_coordinates = []
        for c in cnts:
            area = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)

            if y >= 600 and x <= 1000:
                if area > 10000:
                    image = cv2.rectangle(im, (x, y), (2200, y + h),
                            color=(255, 0, 255), thickness=3)
                    line_items_coordinates.append([(x, y), (2200, y
                            + h)])

            if y >= 2400 and x <= 2000:
                image = cv2.rectangle(im, (x, y), (2200, y + h),
                        color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y + h)])

        return (image, line_items_coordinates)

    def pdf_to_text(
        self,
        pdf_path,
        start_page_num,
        end_page_num,
        dpi,
        resolution=None,
        ):

        pages = convert_from_path(pdf_path=pdf_path, dpi=dpi)
        i = start_page_num - 1
        files = []

        for pag in pages:
            if i == end_page_num:
                break
            if start_page_num == end_page_num:
                filename = 'page_' + str(start_page_num) + '.png'
                files.append(filename)
                pag.save(filename, 'PNG')
            else:
                filename = 'page_' + str(i) + '.png'
                files.append(filename)
                pag.save(filename, 'PNG')
            i += 1
        lists = []
        custom_config = r'--oem 3 --psm 6'
        cv2.ocl.setUseOpenCL(True)
        print ('OpenCL available:', cv2.ocl.haveOpenCL())
        data_select_origin = []

        for con in files:
            data_select_origin.append(self.mark_region(con))



        print(data_select_origin)
                # return data_select_origin
        k=0
        for i in data_select_origin[0]:
        	print(i[k])
        	k+=1
'''
#for j in range(len(data_select_origin[k][1])):
                img = i[0][k].get()
                img
                thresh1 = cv2.threshold(img, 120, 255,
                        cv2.THRESH_BINARY)

                                # pytesseract image to string to get results

                text = pytesseract.image_to_string(img,
                        config='--psm 6')
                print(text)



                                                #re.sub(r"[^a-zA-Z0-9\n\.\@\:\+\-\_\&\*\^\%\)\(\{\}\+\=\#\!\~\'\"\?\,\;\$\₹\€\~\`\<\>\/ ]+", '', dc)+'\n'
                        lists.append(data)
                        os.remove(con)

                return lists



import pandas as pd
import time
path = "D:\\pdf_file_data\\Annexure 5 Datasheet-Tata Project (1).pdf"
p=pdf()
start_time = time.time()
data=p.pdf_to_text(pdf_path=path,start_page_num=0,end_page_num=1,no_of_position_select=1,dpi=140)#[0].split('\n')
print("--- %s seconds ---" % (time.time() - start_time))
filename = path.split('\\')[2]
print(data)
'''
