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

wind_direction_rectangle = ImageRectangle(578, 87, 60, 13)

def UrlToImage(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

def GetWindDirection(radar_img):
    wind_dir_text_image = radar_img[wind_direction_rectangle.y:wind_direction_rectangle.y+wind_direction_rectangle.h, wind_direction_rectangle.x:wind_direction_rectangle.x+wind_direction_rectangle.w]
    direction_recognized_str = image_to_string(wind_dir_text_image, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789HO')
    if(direction_recognized_str == "HO"):
        return "Wind direction is undefined."
    else:
        return "Wind direction is {} degrees (to north direction) .".format(direction_recognized_str)

if __name__ == '__main__':
    img = UrlToImage(radar_image_url)
    print(GetWindDirection(img))
