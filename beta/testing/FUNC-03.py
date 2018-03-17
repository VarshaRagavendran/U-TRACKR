import unittest
import sys
sys.path.append("..")
from tracker import tracker

class TestSameTimeStamp(unittest.TestCase):

    #FUNC-03
    def test_sameTimeStamp(self):
        utrackr2 = tracker('192.168.0.18')
        utrackr4 = tracker('192.168.0.19')
        utrackr3 = tracker('192.168.0.31')
        utrackr = tracker('192.168.0.21')
        rpiOneTimestamp = utrackr.timesync.getTimeStamp()
        rpiTwoTimeStamp = utrackr2.timesync.getTimeStamp()
        rpiThreeTimeStamp = utrackr3.timesync.getTimeStamp()
        rpiFourTimeStamp = utrackr4.timesync.getTimeStamp()
        print "RPi Timestamp 1: " + rpiOneTimestamp
        print "RPi Timestamp 2: " + rpiTwoTimeStamp
        print "RPi Timestamp 3: " + rpiThreeTimeStamp
        print "RPi Timestamp 4: " + rpiFourTimeStamp
        self.assertEquals(rpiOneTimestamp, rpiTwoTimeStamp)
        self.assertEquals(rpiTwoTimeStamp, rpiThreeTimeStamp)
        self.assertEquals(rpiThreeTimeStamp, rpiFourTimeStamp)

if __name__ == '__main__':
    unittest.main()
