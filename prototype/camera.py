import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

kernel = np.ones((5,5),np.uint8)

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_object(self):
        # My experimental values for green ball
        hmn = 0
        hmx = 102
        smn = 55
        smx = 72
        vmn = 0
        vmx = 121
        found_objects = False
        #converting to HSV
        frame = self.flip_if_needed(self.vs.read()).copy() 
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hue,sat,val = cv2.split(hsv)

        # Apply thresholding
        hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
        sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
        vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
        # AND h s and v
        tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
        # Some morpholigical filtering
        dilation = cv2.dilate(tracking,kernel,iterations = 1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing,(5,5),0)
        # Detect circles using HoughCircles
        circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=10,maxRadius=0)
        # circles = np.uint16(np.around(circles))
        

        #Draw Circles
        if circles is not None:
            found_objects = True
            for i in circles[0,:]:
                # If the ball is far, draw it in green
                if int(round(i[2])) < 30:
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
                # else draw it in red
                elif int(round(i[2])) > 35:
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
                    buzz = 1

        #Show the result in frames
       #cv2.imshow('HueComp',hthresh)
        #cv2.imshow('SatComp',sthresh)
        #cv2.imshow('ValComp',vthresh)
        #cv2.imshow('closing',closing)
        #cv2.imshow('tracking',frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)


