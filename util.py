import numpy as np
import cv2

def get_limits(color):
    c=np.uint8([[color]])
    import numpy as np
import cv2

def get_limits(color):
    
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)[0][0]

    lowerLimit = np.array([hsvC[0] - 10, 100, 100], dtype=np.uint8)
    upperLimit = np.array([hsvC[0] + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit