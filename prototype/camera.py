import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import sys
import numpy as np
import os

kernel = np.ones((5,5),np.uint8)

class VideoCamera(object):

    def __init__(self, flip = False):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.flip = flip
        self.video = self.VideoCapture()
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def VideoCapture(self):
        video = cv2.VideoCapture(0)
        video.set(3, 340)
        video.set(4, 240)

        return video

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        # My experimental values for green ball
        hmn = 0
        hmx = 102
        smn = 55
        smx = 72
        vmn = 0
        vmx = 121
        found_objects = False
        #converting to HSV
        # print "in get_object, before converting to HSV"
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # print "in get_object, after converting to HSV"
        hue,sat,val = cv2.split(hsv)

        # Apply thresholding
        # print "in get_object, before applying thresholding"
        hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
        sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
        vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
        # AND h s and v
        tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
        # print "in get_object, after applying thresholding"
        # Some morpholigical filtering
        # print "in get_object, before applying morpholigical filtering"
        dilation = cv2.dilate(tracking,kernel,iterations = 1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing,(5,5),0)
        # print "in get_object, after applying morpholigical filtering"
        # print "in get_object, before detecting using hough circles"
        # Detect circles using HoughCircles
        circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=120,param2=50,minRadius=10,maxRadius=0)
        # circles = np.uint16(np.around(circles))
        # print "in get_object, after detecting using hough circles"

        
        # print "in get_object, before drawing using hough circles"
        #Draw Circles
        if circles is not None:
            # print "can detect circles"
            found_objects = True
            for i in circles[0,:]:
                # If the ball is far, draw it in green
                if int(round(i[2])) < 30:
                    # print "currently drawing a close circle"
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
                # else draw it in red
                elif int(round(i[2])) > 35:
                    # print "currently drawing a far circle"
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
                    buzz = 1

        #print "in get_object, after drawing hough circles"


        #Show the result in frames
        # print "in get_object, before showing result in frames"
        cv2.imshow('HueComp',hthresh)
        cv2.imshow('SatComp',sthresh)
        cv2.imshow('ValComp',vthresh)
        cv2.imshow('closing',closing)
        cv2.imshow('tracking',frame)
        # print "in get_object, before showing result in frames"

        ret, jpeg = cv2.imencode('.jpg', frame)
        # print "before returning the frame"
        return (jpeg.tobytes())
