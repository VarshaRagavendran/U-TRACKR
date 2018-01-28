from collections import deque
import cv2
import numpy as np
import imutils


cap = cv2.VideoCapture();
#IP addr to change depending on Pi
cap.open('tcp://192.168.86.133:5000')


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:

        frame = imutils.resize(frame, width=400)

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space
        greenLower = np.array([29, 86, 6])
        greenUpper = np.array([64, 255, 255])

        # initialize the list of tracked points, the frame counter,
        # and the coordinate deltas
        pts = deque(maxlen=32)
        counter = 0
        (dX, dY) = (0, 0)
        direction = ""

        (grabbed, frame) = cap.read()
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
        
# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
 
