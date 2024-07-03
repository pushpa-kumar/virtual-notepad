import cv2
import math

import numpy as np
from hand_detection import hand_detector
cap=cv2.VideoCapture(0)
hand=hand_detector()

import subprocess

def set_volume(volume_level):
    applescript = f'''
    set volume output volume {volume_level}
    '''
    subprocess.call(['osascript', '-e', applescript])
    


while True:
    success,img=cap.read()
    img = cv2.resize(img, (1300, 700))
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    hand.find_hands(img)

    index=hand.find_position(img)
    dis=0
    if len(index)>0:
        cv2.line(img,(index[4][1],index[4][2]),(index[8][1],index[8][2]),(255,0,0),2)
        cv2.circle(img,(index[4][1],index[4][2]),10,(0,0,255),10)
        cv2.circle(img,(index[8][1],index[8][2]),10,(0,0,255),10)
        cv2.circle(img,(int((index[4][1]+index[8][1])/2),int((index[4][2]+index[8][2])/2)),10,(100,100,100),5)
        dis=math.hypot((index[4][1]-index[8][1]),(index[4][2]-index[8][2]))
    cv2.rectangle(img, (75,75), (125,525), (255, 0, 0), 2)
    
     
    sound=int((2*dis-100)/5)

    if sound<0:
        sound=0
    elif sound>100:
        sound=100
    x,y=100,500
    y=int(500-(4*sound))
    color=(0,0,0)
    if sound >= 0 and sound < 20:
        color=(0,255,0)
    elif sound <=100 and sound>80:
        color=(0,0,255)
    else:
        color=(0,255,255)

    
    print(dis,sound)
    set_volume(sound)
    cv2.rectangle(img, (x-25,y-25), (x+25,y+25), color, -1)
    cv2.putText(img,f"Sound :{sound} %",(800,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()     