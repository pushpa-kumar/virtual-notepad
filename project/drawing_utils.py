import cv2
import numpy as np
import math


def draw_line(canvas, start, end, color, thickness=30):
    cv2.line(canvas, start, end, color, thickness)
 
def erase_area(canvas, center, radius):
    # Create a mask with a circle at the center
    mask = np.zeros(canvas.shape, dtype=np.uint8)
    cv2.circle(mask, center, radius, (255, 255, 255), -1)
    # Invert the mask to create a "hole" in the canvas
    mask = cv2.bitwise_not(mask)
    # Apply the mask to the canvas
    canvas[:] = cv2.bitwise_and(canvas, mask)
    
    
    