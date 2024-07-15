import cv2
import numpy as np
import hand_detection
import drawing_utils
import predict
import ui_utils
import math
import time
import os
class virtal_notepad():
    def __init__(self):
        self.hand = hand_detection.hand_detector()
        self.canvas = np.zeros((720,1280, 3), dtype=np.uint8)
        self.prev_x, self.prev_y = 0, 0
        self.draw_color = (0, 0, 0)
        self.selected_draw=False
        self.selected_erase=False
        self.selected_predict=False
        self.predicted_one=False
        self.selected_clear=False
        self.line_output = ''
        self.dropdown_visible = False
        self.selected_action = ""
        self.img_height=720
        self.img_width=1280
        self.file_opened=False
        
    def mouse_callback(self,event, x, y,flags, param):
        if event == cv2.EVENT_RBUTTONDOWN:
            if  x >1200 and y< self.img_height // 7:
                self.dropdown_visible = not self.dropdown_visible
        elif event == cv2.EVENT_LBUTTONDOWN:
            if self.dropdown_visible:
                if y > 110 and y < 130:
                    self.selected_action = "save"
                    self.dropdown_visible = False
                elif y > 140 and y < 160:
                    self.selected_action = "exit"
                    self.dropdown_visible = False
                elif y > 170 and y < 200:
                    self.selected_action = "help"
                    self.dropdown_visible = False
                    
    
    def run(self):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Virtual notepad")
        cv2.setMouseCallback("Virtual notepad", self.mouse_callback)
        
        while True:
            success,img=cap.read()
            if not success:
                break
                # resizing
            img = cv2.resize(img, (self.img_width,self.img_height))
            # inverting image for convenience 
            img=cv2.flip(img,1)
            # converting into rgb
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # tracks hand
            self.hand.find_hands(img)
            index = self.hand.find_position(img)
            
            ##creating transparent canvas
            mask = np.zeros((720,1280), dtype=np.uint8)
            mask[:] = 255
            
            # Combine the canvas and mask to create a transparent overlay
            overlay = np.zeros((720,1280, 4), dtype=np.uint8)
            overlay[:, :, 0:3] = self.canvas[:, :, 0:3].copy()
            overlay[:, :, 3] = mask
            
            overlay_bgr = cv2.cvtColor(overlay[:, :, 0:3], cv2.COLOR_RGB2BGR)
            overlay_bgr = cv2.resize(overlay_bgr, (self.img_width, self.img_height))
            img = cv2.addWeighted(img, 1, overlay_bgr, 1, 0)
            
            
            ui_utils.selection(img,self.img_height,self.img_width)
            
            if len(index)>0:
                # tracks co-ordinates of index finger
                index_fin = index[8]
                # tracks co-ordinates of middle finger
                middle_fin = index[12]
                
                # this condion satisfies if both index and middle fingers are open 
                # for selecting color or erase or predict or something else
                
                if index_fin[2] > middle_fin[2] and index_fin[1] < middle_fin[1]:
                                
                    
                #----------------------------------------------------------------------------------------------------------------------------------------       
                        # selects color based on middle finger position
                
                    
                    if 370+self.img_height // 7<middle_fin[1] and middle_fin[1] < 2*(self.img_height // 7)+370 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                        self.draw_color=(0,0,255)
                        self.selected_draw=True
                        self.selected_erase=False
                        self.selected_predict=False    
                        self.predicted_one=False
                        self.line_output = ''  
                        self.selected_clear=False         
                    elif 400+2*(self.img_height // 7)<middle_fin[1] and middle_fin[1] < 3*(self.img_height // 7)+400 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                        self.draw_color=(0,255,0)
                        self.selected_draw=True
                        self.selected_erase=False
                        self.selected_predict=False 
                        self.predicted_one=False   
                        self.line_output = '' 
                        self.selected_clear=False
                    elif 430+3*(self.img_height // 7)<middle_fin[1] and middle_fin[1] < 4*(self.img_height // 7)+430 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                        self.draw_color=(255,255,255)
                        self.selected_draw=True
                        self.selected_erase=False
                        self.selected_predict=False 
                        self.predicted_one=False 
                        self.line_output = '' 
                        self.selected_clear=False  
                    elif 460+4*(self.img_height // 7)<middle_fin[1] and middle_fin[1] < 5*(self.img_height // 7)+460 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                        self.draw_color=(255,0,0)
                        self.selected_draw=True
                        self.selected_erase=False
                        self.selected_predict=False  
                        self.predicted_one=False  
                        self.line_output = '' 
                        self.selected_clear=False
                    elif 670+4*(self.img_height // 7)<middle_fin[1] and middle_fin[1] < 5*(self.img_height // 7)+670 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                        self.selected_draw=False
                        self.selected_erase=True
                        self.selected_predict=False 
                        self.predicted_one=False  
                        self.line_output = '' 
                        self.selected_clear=False 
                        
                if self.selected_draw==True:
                    if self.draw_color==(0,0,255):
                        cv2.rectangle(img,(370+self.img_height // 7,0),(2*(self.img_height // 7)+370,self.img_height // 7),(150,135,240),5)
                    elif self.draw_color==(0,255,0):
                        cv2.rectangle(img,(400+2*(self.img_height // 7),0),(3*(self.img_height // 7)+400,self.img_height // 7),(150,135,240),5)
                    elif self.draw_color==(255,255,255):
                        cv2.rectangle(img,(430+3*(self.img_height // 7),0),(4*(self.img_height // 7)+430,self.img_height // 7),(150,135,240),5)            
                    elif self.draw_color==(255,0,0):
                        cv2.rectangle(img,(460+4*(self.img_height // 7),0),(5*(self.img_height // 7)+460,self.img_height // 7),(150,135,240),5)
                        
                
                        # if distance blw present and previous point is >5 it draws and when middle finger is opened initial value resets to 0
                if self.selected_draw==True:
                    # to drw you need to close middle finger and raw with index finger only
                    if index_fin[2] < middle_fin[2] and index_fin[1] < middle_fin[1]:
                        
                        if prev_x == 0 and prev_y == 0:
                            prev_x, prev_y = index_fin[1], index_fin[2]
                        else:
                            dis = int(math.hypot(index_fin[1] - prev_x, index_fin[2] - prev_y))
                            if dis > 5:
                                drawing_utils.draw_line(self.canvas, (prev_x, prev_y), (index_fin[1], index_fin[2]), self.draw_color)
                                prev_x, prev_y = index_fin[1], index_fin[2]
                    else:
                        prev_x = 0
                        prev_y = 0
                        
                
                            # for erasing select eraser with middle finger and erase with index finger
        
                if self.selected_erase==True:
                    cv2.rectangle(img,(670+4*(self.img_height // 7),0),(5*(self.img_height // 7)+670,self.img_height // 7),(150,135,240),5)
                    
                    if index_fin[2] < middle_fin[2] and index_fin[1]< middle_fin[1]:
                        drawing_utils.erase_area(self.canvas,(index_fin[1],index_fin[2]),20) 
                        
                
                            
                # selecting predict
                if 230<middle_fin[1] and middle_fin[1] < 400 and 0<middle_fin[2] and middle_fin[2]<self.img_height // 7:
                    
                    self.selected_draw=False
                    self.selected_erase=False
                    self.selected_predict=True
                    self.selected_clear=False
                
                # selecting clear
                if 35<middle_fin[1] and middle_fin[1]<160 and 0<middle_fin[2] and middle_fin[2] < self.img_height//7:
                    self.selected_draw=False
                    self.selected_erase=False
                    self.selected_predict=False
                    self.selected_clear=True
                    self.line_output = ''
                    self.predicted_one=False      
            
            save_canvas="canvas.png"
            cv2.imwrite(save_canvas,self.canvas)
            
            if self.selected_clear==True:
                cv2.rectangle(img,(35,0),(160,self.img_height // 7),(150,135,240),5)
                self.canvas[:] = 0
                prev_x = 0
                prev_y = 0 
                
            if self.selected_predict==True:
                cv2.rectangle(img,(230,0),(400,self.img_height // 7),(150,135,240),5)  
            
            if self.selected_predict==True:        
                if self.predicted_one==False:
                    self.predicted_one=True
                    predict_image=cv2.imread('canvas.png')
                    gray = cv2.cvtColor(predict_image, cv2.COLOR_BGR2GRAY)
                    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
                    
                    # Loop through the contours and crop the image around each contour
                    for i, contour in enumerate(contours):
                        # Get the bounding box for each contour
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Crop the image using the bounding box coordinates
                        cropped_image = predict_image[y:y+h, x:x+w]
                        
                        # Predict the letter
                        # pre_process=preprocess_image(cropped_image)
                        predicted_letter = predict.predict_letter(cropped_image)
                        character='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                        self.line_output += character[predicted_letter]
                
                
                    #----------------------------------------------------------------------------------------------------------------------------------------            
                cv2.rectangle(img, (0, 650), (self.img_width, self.img_height), (0, 0, 0), -1)
                cv2.putText(img, f'PREDICTION:{self.line_output}', (200, 690), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255,100), 3)
                
            if self.dropdown_visible:
                cv2.rectangle(img, (1180, self.img_height //7), (1280, self.img_height//7 + 100), (255, 255, 255), -1)
                cv2.putText(img, "save", (1185, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
                cv2.putText(img, "exit", (1185, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
                cv2.putText(img, "help", (1185, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
                
            if self.selected_action == "save":
                timestamp = time.time()
                save_written=f"canvas{timestamp}.png"
                cv2.imwrite(save_written,self.canvas)
                break
            elif self.selected_action == "exit":
                break
            elif self.selected_action=="help":
                if not self.file_opened:
                    self.file_opened=True
                    file_path='instructions.pdf'
                    os.system('open ' + file_path)
                            
            cv2.imshow("Virtual notepad", img)


            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
            
            
             
        
        
def main():
    notepad = virtal_notepad()
    notepad.run()
           
if __name__ == "__main__":
    main()
        