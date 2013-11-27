# P2N - play numeric music depending on the physical object presented to the webcam

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import cv2, math
import cv2
import numpy as np

#cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

COLOR_MIN = np.array([20, 80, 80], np.uint8)
COLOR_MAX = np.array([40, 255, 255], np.uint8)

while rval:
    #cv2.imshow("preview", frame)
    rval, frame = vc.read()

    # invert color
    frame = cv2.medianBlur(frame, 5)
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # flaten
    #frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)

    # get contours
    ret, thresh = cv2.threshold(hsv_img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]
    if len(areas) > 0:
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(hsv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Show", hsv_img)

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
            break

cv2.destroyAllWindows()
cv2.VideoCapture(0).release()
