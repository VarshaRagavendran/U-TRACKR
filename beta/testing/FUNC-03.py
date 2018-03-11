import unittest
import time
import sys
sys.path.append("..")
from tracker import tracker
from timesync import timesync
from checker import checker

class TestSameTimeStamp(unittest.TestCase):

    #FUNC-03
    def test_sameTimeStamp(self):
        utrackr2 = tracker('192.168.0.18')
        utrackr4 = tracker('192.168.0.19')
        utrackr3 = tracker('192.168.0.31')
        utrackr = tracker('192.168.0.21')
        self.assertEquals(utrackr.timesync.getTimeStamp() ,utrackr2.timesync.getTimeStamp())
        self.assertEquals(utrackr2.timesync.getTimeStamp() ,utrackr3.timesync.getTimeStamp())
        self.assertEquals(utrackr3.timesync.getTimeStamp() ,utrackr4.timesync.getTimeStamp())


if __name__ == '__main__':
    unittest.main()
