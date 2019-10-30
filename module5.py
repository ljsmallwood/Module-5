import numpy as np
import math
import cv2
import time
from picamera import PiCamera
import RPi.GPIO as GPIO

#take a picture
camera = PiCamera()
camera.rotation = 180
#def cameraOn():
camera.capture("/home/pi/Desktop/ball5.jpg")

# show image
img =cv2.imread("/home/pi/Desktop/ball5.jpg")
print (img.size)
print (img.shape)
cv2.imshow("ball3",img)
cv2.destroyAllWindows()

# change size
new_width = int(img.shape[1]/2)
new_height = int(img.shape[0]/2)
smaller = cv2.resize(img, (new_width,new_height), interpolation =cv2.INTER_AREA)
cv2.imwrite('smallball.png', smaller)

# change from BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imwrite('hsv_ball3.png',hsv)
mask = cv2.inRange(hsv, (100, 150, 0),(135, 255, 255))
cv2.imwrite('mask_ball3.png',mask)

# locate color
M = cv2.moments(mask)
print (M["m00"])
print (M["m01"])
print (M["m10"])
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
print ("Center: (%s , %s)" % (cX, cY))

# locate color region
mask = cv2.blur(mask,(5,5))
thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite('ball3_thresh.png', thresh)


# convolution of pixels
M = cv2.moments(thresh)
cX = int(M["m10"] /M["m00"])
cY = int(M["m01"] /M["m00"])
print ("Center: (%s , %s)" % (cX, cY))

#calc angle from camera to ball
angle = (360/math.pi)
angle2 = 90 -(angle *(math.atan(float(cY)/float(cX))))
if angle2 > 0:
	print("Angle: %s" %angle2)
elif angle2 < 0:
#	angle2 = 90 +(angle*(math.atan(float(cY)/float(cX))))
	angle2 = abs(angle2) + 90
	print("Angle: %s" %angle2)

# put circle on cm picture
img =cv2.imread("/home/pi/Desktop/ball5.jpg")
cv2.circle(img,(cX,cY),40,(0,255,255),2)
cv2.imshow("ballcircle",img)
time.sleep(2)
cv2.imwrite("/home/pi/Desktop/ball5.jpg",img)
