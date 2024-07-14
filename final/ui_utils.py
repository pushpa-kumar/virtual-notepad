import cv2
import numpy as np


def rectangular_bar(img,height,width):
    cv2.rectangle(img, (0, 0), (width, height // 7), (0, 0, 0), -1)


def display_photos(img,height):
    # load photos
    blue=cv2.imread("images/blue.png")
    green=cv2.imread("images/green.png")
    white=cv2.imread("images/white.png")
    red=cv2.imread("images/red.png")
    erase=cv2.imread("images/erase.png")
    more=cv2.imread("images/more.png")
    
    # resizing photos
    blue_resized=cv2.resize(blue,(height // 7,height // 7))
    green_resized=cv2.resize(green,(height // 7,height // 7))
    white_resized=cv2.resize(white,(height // 7,height // 7))
    red_resized=cv2.resize(red,(height // 7,height // 7))
    erase_resized=cv2.resize(erase,(height // 7,height // 7))
    more_resized=cv2.resize(more,(80,height // 7))
    
    img[0:height // 7,370+height // 7:2*(height // 7)+370] = blue_resized[:,:,:3]
    img[0:height // 7,400+2*(height // 7):3*(height // 7)+400] = green_resized[:,:,:3]   
    img[0:height // 7,430+3*(height // 7):4*(height // 7)+430] = white_resized[:,:,:3]   
    img[0:height // 7,460+4*(height // 7):5*(height // 7)+460] = red_resized[:,:,:3]   
    img[0:height // 7,670+4*(height // 7):5*(height // 7)+670] = erase_resized[:,:,:3]   
    img[0:height // 7,1200:1280] = more_resized[:,:,:3]   
    
    cv2.putText(img, 'PREDICT', (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200,100), 3) 
    cv2.putText(img, 'CLEAR', (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100,100), 3)       

    
def selection(img,height,width):
    rectangular_bar(img,height,width)
    display_photos(img,height)
    