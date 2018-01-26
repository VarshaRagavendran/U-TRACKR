import cv2
import numpy as np

cap = cv2.VideoCapture();
cap.open('tcp://192.168.1.195:5000')


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        #frame = cv2.flip(frame, 0)
        cv2.imshow('frame', frame)

        # write the flipped frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #else:
     #   break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
 

