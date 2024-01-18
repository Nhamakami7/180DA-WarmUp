import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Color order: blue, green, red
    lower_color_bound = (100, 0, 0)
    upper_color_bound = (255, 80, 80)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(frame, lower_color_bound, upper_color_bound)
    # mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # frame = frame | mask_rgb

    contours, _ = cv2.findContours(mask, 1, 2)
    
    # Draw bounding box if any color within threshold was found
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(max_contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('Video feed', frame)
    # cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# References: https://ckyrkou.medium.com/color-thresholding-in-opencv-91049607b06d