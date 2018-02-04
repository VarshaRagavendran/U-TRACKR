from threading import Thread
from tracker import tracker
import time

utrackr = tracker('192.168.1.207')
utrackr2 = tracker('192.168.0.39')

def func1():
    while (utrackr.cap.isOpened()):
        print "cam1: " + utrackr.timesync.getTimeStamp() + " x: " + str(utrackr.x) + " y: " + str(utrackr.y)
        time.sleep(1)

def func2():
    utrackr.outputFrame("frame1")

def func3():
    while (utrackr2.cap.isOpened()):
        print "cam2: " + utrackr2.timesync.getTimeStamp() + " x: " + str(utrackr2.x) + " y: " + str(utrackr2.y)
        time.sleep(1)

def func4():
    utrackr2.outputFrame("frame2")

if __name__=='__main__':
	Thread(target = func1).start()
	Thread(target = func2).start()
	Thread(target = func3).start()
	Thread(target = func4).start()