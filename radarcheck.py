import numpy as np
import cv2
import urllib.request
from pytesseract import image_to_string

radar_image_url = 'http://meteoinfo.by/radar/UKBB/UKBB_latest.png'

class ImageRectangle:
    x = 0
    y = 0
    w = 1
    h = 1
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def UrlToImage(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def CropImage(img, rect):
    return img[rect.y:rect.y+rect.h, rect.x:rect.x+rect.w]


def RecognizeNumberStr(img):
    return image_to_string(img, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789HO')


def RecognizedNumberUndefined(str):
    if(recognized_str == "" or 'H' in recognized_str):
        return true
    return false


def GetWindDirection(radar_img):
    rect = ImageRectangle(578, 87, 60, 13)
    cropped_img = CropImage(radar_img, rect)
    recognized_str = RecognizeNumberStr(cropped_img)
    if(RecognizedNumberUndefined(recognized_str)):
        return "Wind direction is undefined."
    else:
        return "Wind direction is {} degrees (from north direction) .".format(recognized_str)

def GetWindSpeed(radar_img):
    rect = ImageRectangle(585, 101, 50, 13)
    cropped_img = CropImage(radar_img, rect)

    recognized_str = RecognizeNumberStr(cropped_img)
    if(RecognizedNumberUndefined(recognized_str)):
        return "Wind speed is undefined."
    else:
        return "Wind speed is {} kmph .".format(recognized_str)

if __name__ == '__main__':
    img = UrlToImage(radar_image_url)
    print(GetWindDirection(img))
    print(GetWindSpeed(img))
