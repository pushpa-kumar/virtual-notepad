import mediapipe
import cv2
from hand_detection import hand_detector

cap=cv2.VideoCapture(0)
hand=hand_detector()
paused = False
while True:
    success,img=cap.read()
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    hand.find_hands(img)
    if paused:
        x, y = 50, 70
        cv2.putText(img, "PAUSE", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)    
    cv2.imshow("image",img) 
    key = cv2.waitKey(1) & 0xFF
    index=hand.find_position(img)
    score=0

    if len(index) >0: 
        if index[1][1]>index[0][1]:
            if index[3][1]<index[4][1]:
                score+=1
        else:
            if index[3][1]>index[4][1]:
                score+=1
        if index[6][2] > index[8][2]:
            score+=1   
        if index[10][2] > index[12][2]:
            score+=1 
        if index[14][2] > index[16][2]:
            score+=1
        if index[18][2] > index[20][2]:
            score+=1

    if score >= 4:
        paused = True
        img_paused=img
    else:
        paused = False

    if paused:
        while True:
            success, img = cap.read()
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hand.find_hands(img)
            index = hand.find_position(img)
            score=0
            x, y = 50, 70
            cv2.putText(img_paused, "PAUSE", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)    
            if len(index) >0: 
                if index[1][1]>index[0][1]:
                    if index[3][1]<index[4][1]:
                        score+=1
                else:
                    if index[3][1]>index[4][1]:
                        score+=1
                if index[6][2] > index[8][2]:
                    score+=1   
                if index[10][2] > index[12][2]:
                    score+=1 
                if index[14][2] > index[16][2]:
                    score+=1
                if index[18][2] > index[20][2]:
                    score+=1
                cv2.imshow("image",img_paused)
            key = cv2.waitKey(1) & 0xFF
            if score<4:
                paused=False
                break
            if key == ord('q'):
                break
        
    
    if key == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()   