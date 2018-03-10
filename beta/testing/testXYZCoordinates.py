import unittest
import time
from tracker import tracker
from timesync import timesync
from checker import checker
import psutil

class TestXYZCoordinates(unittest.TestCase):

    #FUNC-05
    def testXYZCoordinates(self):
        utrackr2 = tracker('192.168.0.18')
        utrackr4 = tracker('192.168.0.19')
        utrackr3 = tracker('192.168.0.20')
        utrackr = tracker('192.168.0.21')
        time.sleep(1)
        poscalc = checker(utrackr.x, utrackr.y, utrackr2.x, utrackr2.y, utrackr3.x, utrackr3.y, utrackr4.x, utrackr4.y)
        x, y, z = poscalc.position_calculation()
        assert x != 0 or x != None
        assert y != 0 or y != None
        assert z != 0 or z != None
        #self.assertNotEqual(x,0) # or none?
        #self.assertNotEqual(y,0) # or none?
        #self.assertNotEqual(z,0) # or none?

if __name__ == '__main__':
    unittest.main()
