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
                # define the lower and upper boundaries of the "green"
                # ball in the HSV color space
                greenLower = np.array([29, 86, 6])
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

    def outputFrame(self, frameName):
        while (self.cap.isOpened()):
            cv2.imshow(frameName, self.getFrame())
            key = cv2.waitKey(1) & 0xFF

    def tracker(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                # define the lower and upper boundaries of the "green"
                # ball in the HSV color space
                greenLower = np.array([29, 86, 6])
                greenUpper = np.array([64, 255, 255])

                # initialize the list of tracked points, the frame counter,
                # and the coordinate deltas
                pts = deque(maxlen=32)
                # counter = 0
                # (dX, dY) = (0, 0)
                # direction = ""

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
           
                    # show the movement deltas and the direction of movement on
                    # the frame
                    #cv2.putText(frame, "x: {}, y: {}, radius: {}".format(x, y, radius),
                    #    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    #    0.6, (0, 0, 255), 1)

                # show the frame to our screen and increment the frame counter
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

    #<todo> find out why this crashes
    def hsvModifier(self):
        kernel = np.ones((5,5),np.uint8)
        while(True):
            ret, frame = self.cap.read()
            # Creating a windows for later use
            cv2.namedWindow('HueComp', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('HueComp', 300, 300)
            cv2.namedWindow('SatComp', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('SatComp', 300, 300)
            cv2.namedWindow('ValComp', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('ValComp', 300, 300)
            cv2.namedWindow('closing', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('closing', 300, 300)
            cv2.namedWindow('tracking', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('tracking', 480, 320)

            # Creating track bar for min and max for hue, saturation and value
            # You can adjust the defaults as you like
            cv2.createTrackbar('hmin', 'HueComp',0,255, lambda x:x)
            cv2.createTrackbar('hmax', 'HueComp',120,255, lambda x:x)

            cv2.createTrackbar('smin', 'SatComp',8,255, lambda x:x)
            cv2.createTrackbar('smax', 'SatComp',100,255, lambda x:x)

            cv2.createTrackbar('vmin', 'ValComp',27,255, lambda x:x)
            cv2.createTrackbar('vmax', 'ValComp',100,255, lambda x:x)

            frame = imutils.resize(frame, width=400)

            # define the lower and upper boundaries of the "green"
            # ball in the HSV color space

            # initialize the list of tracked points, the frame counter,
            # and the coordinate deltas
            pts = deque(maxlen=32)
            counter = 0
            (dX, dY) = (0, 0)
            direction = ""

            (grabbed, frame) = self.cap.read()
            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600)
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hue,sat,val = cv2.split(hsv)

            # get info from track bar and appy to result
            hmn = cv2.getTrackbarPos('hmin','HueComp')
            hmx = cv2.getTrackbarPos('hmax','HueComp')
            

            smn = cv2.getTrackbarPos('smin','SatComp')
            smx = cv2.getTrackbarPos('smax','SatComp')


            vmn = cv2.getTrackbarPos('vmin','ValComp')
            vmx = cv2.getTrackbarPos('vmax','ValComp')

            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            lower = np.array([hmn, smn, vmn])
            upper = np.array([hmx, smx, vmx])
            mask = cv2.inRange(hsv, lower, upper)
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
       
                # show the movement deltas and the direction of movement on
                # the frame
                #cv2.putText(frame, "x: {}, y: {}, radius: {}".format(x, y, radius),
                #    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                #    0.6, (0, 0, 255), 1)

            # show the frame to our screen and increment the frame counter
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

                # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

    def stopTracker(self):
        # Release everything if job is finished
        self.cap.release()
        cv2.destroyAllWindows()