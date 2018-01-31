from timesync import timesync
import cv2

t = timesync('192.168.1.248')
t.runRaspiVid()

while True:
    k = cv2.waitKey(1) & 0xFF
    #press 'q' to exit
    if k == ord('q'):
        break
    print t.getTimeStamp()

t.closeSSHClient()