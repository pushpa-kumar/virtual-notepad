import cv2
import math
import numpy as np
from hand_detection import hand_detector

cap=cv2.VideoCapture(0)
hand=hand_detector()
x,y=0,0
coo=[]
selected=False
while True:
    success,img=cap.read()
    img = cv2.resize(img, (1200, 700))
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    hand.find_hands(img)
    sword=cv2.imread('sword.jpeg')
     

    img_resized = cv2.resize(sword, (100, 200))

    
    index=hand.find_position(img)
    dis=0
    c_x=0
    c_y=0
    if len(index)>0:
        dis=int(math.hypot((index[4][1]-index[8][1]),(index[4][2]-index[8][2])))           
        c_x,c_y=((index[4][1]+index[8][1])/2),((index[4][2]+index[8][2])/2)
        # print(c_x,c_y)
    
    
    h, w = img_resized.shape[:2]
    img[y:y+h,x:x+w] = img_resized[:,:,:3]
    
    if dis<=50:
        if c_x < (x + w) and c_x > x and c_y < (y + h) and c_y > y:
            selected=True
            coo.append([c_x,c_y])
    else:
        selected=False
    
    
    # if dis <= 50 and c_x < (x + w) and c_x > x and c_y < (y + h) and c_y > y:
    #     selected=True
    #     coo.append([c_x,c_y])
    # else:
    #     selected=False
        
    if selected:
        if len(coo)>=2:
            first=coo[-2]
            second=coo[-1]
            print(first,second)
            # c_x_new,c_y_new=((index[4][1]+index[8][1])/2),((index[4][2]+index[8][2])/2)
            x_mov=int(second[0]-first[0])
            y_mov=int(second[1]-first[1])
            
            x+=x_mov  
            y+=y_mov
            if x<0:
                x=0
            if y<0:
                y=0
            if x>1100:
                x=1100
            if y>500:
                y=500
    # print(x,y)
    cv2.imshow("image", img)

    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 