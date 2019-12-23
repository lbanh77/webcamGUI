# Author: Linda Banh
# The purpose of this code is to use automatically detect bounds for canny thresholds. 
# This code was modified and adapted from this article: 
# https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/

import numpy as np 
import cv2 

def auto_canny(image, sigma=0.33): 
    med = np.median(image)
    threshold1 = int(max(0, (1.0 - sigma)*med))
    threshold2 = int(min(255, (1.0 + sigma)*med))
    return cv2.Canny(image, threshold1, threshold2)