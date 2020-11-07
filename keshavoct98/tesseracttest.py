from PIL import Image, ImageFilter
from pytesseract import *
import numpy as np
import cv2
import matplotlib.pyplot as plt

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

print("pre trained data")
for i in range(0,80):
    filename = r"C:\Users\NA\Desktop\AI_School\Main_project\vision\vision30\tesseract_data\kor.platefont.exp"+str(i)+".jpg"
    # image = Image.open(filename)
    # image = image.filter(ImageFilter.GaussianBlur())
    # img = np.asarray(image)

    img = cv2.imread(filename)
    height, width, channel = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

    img_thresh = cv2.adaptiveThreshold(
        img_blurred, 
        maxValue=255.0, 
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        thresholdType=cv2.THRESH_BINARY_INV, 
        blockSize=19, 
        C=9
    )

    cv2.imwrite(filename, img_thresh)
    # contours, _ = cv2.findContours(
    #     img_thresh, 
    #     mode=cv2.RETR_LIST, 
    #     method=cv2.CHAIN_APPROX_SIMPLE
    # )

    # temp_result = np.zeros((height, width, channel), dtype=np.uint8)
    # cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))

    # cv2.imshow('preprocessing image', img_thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    text = image_to_string(img_thresh, lang="kor")
    print(text)