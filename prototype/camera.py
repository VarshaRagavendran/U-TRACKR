import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import sys
import numpy as np
import os
import argparse
from collections import deque

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
        # return which function you want to perform from the below
        # return self.ball_tracker();
	return self.object_movement_tracker();

    # function for tracking the motion of a green ball (U-TRACKR ALPHA V0.3)
    def object_movement_tracker(self):
        success, frame = self.video.read()
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)

        # initialize the list of tracked points, the frame counter,
        # and the coordinate deltas
        pts = deque(maxlen=32)
        counter = 0
        (dX, dY) = (0, 0)
        direction = ""

        (grabbed, frame) = self.video.read()
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

       # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)
            for i in np.arange(1, len(pts)):
                thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

            # show the movement deltas and the direction of movement on
            # the frame
            cv2.putText(frame, "x: {}, y: {}, radius: {}".format(x, y, radius),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 255), 1)

        # show the frame to our screen and increment the frame counter
        cv2.imshow("Frame", frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes())        

    # function for tracking a green ball (U-TRACKR ALPHA V0.2)
    def ball_tracker(self):
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
        cv2.imshow('HueComp',hthresh)
        cv2.imshow('SatComp',sthresh)
        cv2.imshow('ValComp',vthresh)
        cv2.imshow('closing',closing)
        cv2.imshow('tracking',frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes())