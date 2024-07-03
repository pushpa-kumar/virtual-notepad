import mediapipe as mp
import cv2
class hand_detector():  
    def __init__(self,static_mode=False,no_hands=2,min_detection=0.5,min_tracking=0.5):
        self.static_mode=static_mode
        self.no_hands=no_hands
        self.min_detection=min_detection
        self.min_tracking=min_tracking
        self.mp_hands=mp.solutions.hands
        self.hands=self.mp_hands.Hands()
        self.draw_hand=mp.solutions.drawing_utils
    
    
    def find_hands(self,img):
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for each_hand in self.results.multi_hand_landmarks:
                self.draw_hand.draw_landmarks(img, each_hand,self.mp_hands.HAND_CONNECTIONS)
                
    
    def find_position(self,img,hand_no=0):
        track_point=[]
        if self.results.multi_hand_landmarks:
            req_hand=self.results.multi_hand_landmarks[hand_no]
            for id,lm in enumerate(req_hand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                track_point.append([id,cx,cy])
        return track_point