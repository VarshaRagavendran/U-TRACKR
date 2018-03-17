from threading import Thread
import unittest
import sys
import time
sys.path.append("..")
from tracker import tracker
from checker import checker

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

class TestXYZCoordinates(unittest.TestCase):

    #FUNC-05
    def testXYZCoordinates(self):
        # Wait 5 seconds for U-TRACKR to capture the X and Y values
        time.sleep(5)
        poscalc = checker(utrackr.x, utrackr.y, utrackr2.x, utrackr2.y, utrackr3.x, utrackr3.y, utrackr4.x, utrackr4.y)
        x, y, z = poscalc.position_calculation()
        print "Position Calc (X,Y,Z): " + str(x) + "," + str(y) + "," + str(z) + ")"
        self.assertNotEqual(x, 0)
        self.assertNotEqual(y, 0)
        self.assertNotEqual(z, 0)

if __name__ == '__main__':
    Thread(target=func1).start()
    Thread(target=func2).start()
    Thread(target=func3).start()
    Thread(target=func4).start()
    unittest.main()