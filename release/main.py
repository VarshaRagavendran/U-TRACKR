from threading import Thread
from tracker import tracker
from checker import checker
import time

# # pi camera 1
# utrackr = tracker('192.168.0.25')
#
# # pi camera 2
# utrackr2 = tracker('192.168.0.26')

# # pi camera 4
# utrackr4 = tracker('192.168.0.26')

# pi camera 3
utrackr3 = tracker('192.168.0.29')

# def func1():
#     while (utrackr.cap.isOpened()):
#         print "cam1: " + utrackr.timesync.getTimeStamp() + " x: " + str(utrackr.x) + " y: " + str(utrackr.y)
#         time.sleep(1)
#
# def func2():
#     utrackr.outputFrame("cam1")
#
# def func3():
#     while (utrackr2.cap.isOpened()):
#         print "cam2: " + utrackr2.timesync.getTimeStamp() + " x: " + str(utrackr2.x) + " y: " + str(utrackr2.y)
#         time.sleep(1)
#
# def func4():
#     utrackr2.outputFrame("cam2")

def func5():
    while (utrackr3.cap.isOpened()):
        print "cam3: " + utrackr3.timesync.getTimeStamp() + " x: " + str(utrackr3.x) + " y: " + str(utrackr3.y)
        time.sleep(1)

def func6():
    utrackr3.outputFrame("cam3")

# def func7():
#     while (utrackr4.cap.isOpened()):
#         print "cam4: " + utrackr4.timesync.getTimeStamp() + " x: " + str(utrackr4.x) + " y: " + str(utrackr4.y)
#         time.sleep(1)
#
# def func8():
#     utrackr4.outputFrame("cam4")
#
# def func9():
#     while True:
#         time.sleep(1)
#         poscalc = checker(utrackr.x, utrackr.y, utrackr2.x, utrackr2.y, utrackr3.x, utrackr3.y, utrackr4.x, utrackr4.y)
#         x, y, z = poscalc.position_calculation()
#         print utrackr.timesync.getTimeStamp() + " x: " + str(x) + " y: " + str(y) + " z: " + str(z)

if __name__=='__main__':
    # Thread(target = func1).start()
    # Thread(target = func2).start()
    # Thread(target = func3).start()
    # Thread(target = func4).start()
    #Thread(target = func5).start()
    Thread(target = func6).start()
    # Thread(target = func7).start()
    # Thread(target = func8).start()
    #Thread(target=func9).start()