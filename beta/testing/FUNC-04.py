from threading import Thread
import unittest
import sys
import time
sys.path.append("..")
from tracker import tracker

utrackr = tracker('192.168.0.21')
utrackr2 = tracker('192.168.0.18')
utrackr3 = tracker('192.168.0.31')
utrackr4 = tracker('192.168.0.19')

def func1():
    utrackr.outputFrame("cam1")

def func2():
    utrackr2.outputFrame("cam2")

def func3():
    utrackr3.outputFrame("cam3")

def func4():
    utrackr4.outputFrame("cam4")

class TestObjectIdentified(unittest.TestCase):

    #FUNC-04
    def testObjectIdentified(self):
        # Wait 5 seconds for U-TRACKR to capture the X and Y values
        time.sleep(5)

        # Identification of object's X and Y coordinates from frame is not 0.
        print "RPi 1 (x,y): (" + str(utrackr.x) + "," + str(utrackr.y) + ")"
        print "RPi 2 (x,y): (" + str(utrackr2.x) + "," + str(utrackr2.y) + ")"
        print "RPi 3 (x,y): (" + str(utrackr3.x) + "," + str(utrackr3.y) + ")"
        print "RPi 4 (x,y): (" + str(utrackr4.x) + "," + str(utrackr4.y) + ")"

        self.assertNotEqual(utrackr.x, 0)
        self.assertNotEqual(utrackr.y, 0)

        self.assertNotEqual(utrackr2.x, 0)
        self.assertNotEqual(utrackr2.y, 0)

        self.assertNotEqual(utrackr3.x, 0)
        self.assertNotEqual(utrackr3.y, 0)

        self.assertNotEqual(utrackr4.x, 0)
        self.assertNotEqual(utrackr4.y, 0)

if __name__ == '__main__':
    Thread(target=func1).start()
    Thread(target=func2).start()
    Thread(target=func3).start()
    Thread(target=func4).start()
    unittest.main()