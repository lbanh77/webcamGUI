import numpy as np 
import cv2 

def auto_canny(image, sigma=0.33): 
    med = np.median(image)
    threshold1 = int(max(0, (1.0 - sigma)*med))
    threshold2 = int(min(255, (1.0 + sigma)*med))
    return cv2.Canny(image, threshold1, threshold2)