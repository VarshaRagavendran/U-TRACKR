from collections import deque
from timesync import timesync
import cv2
import numpy as np
import imutils

class tracker(object):

    def __init__(self, ip):
        self.timesync = timesync(ip)
        self.timesync.runRaspiVid()
        self.cap = cv2.VideoCapture();
        self.cap.open('tcp://' + ip + ':5000')
        self.x = 0
        self.y = 0
        self.radius = 0

    def printTimeStamp(self):
        while(self.cap.isOpened()):
            print self.timesync.getTimeStamp()

    def getFrame(self):
        frame = np.zeros(shape=(600, 400, 3)).astype('uint8')
        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                greenLower = np.array([25, 70, 6])
                greenUpper = np.array([64, 255, 255])

                # initialize the list of tracked points, the frame counter,
                # and the coordinate deltas
                pts = deque(maxlen=32)
                # counter = 0
                # (dX, dY) = (0, 0)
                # direction = ""

                # (grabbed, frame) = self.cap.read()
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
                    ((self.x, self.y), self.radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # only proceed if the radius meets a minimum size
                    if self.radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(self.x), int(self.y)), int(self.radius),
                                   (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)

                # loop over the set of tracked points
                for i in xrange(1, len(pts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if pts[i - 1] is None or pts[i] is None:
                        continue

                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
                    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        return frame

    def getFrameARUCO(self):
        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
            frame = imutils.resize(frame, width=600)
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
            parameters = cv2.aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
            #print(corners)
            gray = cv2.aruco.drawDetectedMarkers(frame, corners)
        return gray

    def outputFrame(self, frameName):
        while (self.cap.isOpened()):
            cv2.imshow(frameName, self.getFrame())
            key = cv2.waitKey(1) & 0xFF

    def outputFrameARUCO(self, frameName):
        while (self.cap.isOpened()):
            cv2.imshow(frameName, self.getFrameARUCO())
            key = cv2.waitKey(1) & 0xFF

    def captureFrame(self, frameName):
        ret, frame = self.cap.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("frame%d.jpg" % ret, frame)
        cv2.imshow('frame', gray)

    def stopTracker(self):
        # Release everything if job is finished
        self.cap.release()
        cv2.destroyAllWindows()