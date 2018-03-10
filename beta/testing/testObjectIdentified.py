import unittest
import time
from tracker import tracker
from timesync import timesync
from checker import checker
import psutil

class TestObjectIdentified(unittest.TestCase):

    #FUNC-04
    def testObjectIdentified(self):
        try:
            utrackr2 = tracker('192.168.0.18')
            utrackr4 = tracker('192.168.0.19')
            utrackr3 = tracker('192.168.0.20')
            utrackr = tracker('192.168.0.21')
            #verification that opencv runs smoothly
            utrackr.outputFrame("cam1")
            utrackr2.outputFrame("cam2")
            utrackr3.outputFrame("cam3")
            utrackr4.outputFrame("cam4")

            #identification of object x , y coordinate from frame is not 0.
            if utrackr.radius > 0:
                self.assertNotEqual(utrackr.x,0)
                self.assertNotEqual(utrackr.y,0)

                self.assertNotEqual(utrackr2.x,0)
                self.assertNotEqual(utrackr2.y,0)

                self.assertNotEqual(utrackr3.x,0)
                self.assertNotEqual(utrackr3.y,0)

                self.assertNotEqual(utrackr4.x,0)
                self.assertNotEqual(utrackr4.y,0)
            else:
                self.fail('Object not detected')

        except Exception as e:
            self.fail('Unexpected exception raised', e)


if __name__ == '__main__':
    unittest.main()
