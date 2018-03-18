import unittest
import sys
sys.path.append("..")
from timesync import timesync

class testCPUUsage(unittest.TestCase):

    #PER-04
    def testBitrateUsage(self):
        timesync1 = timesync('192.168.0.21')
        timesync2 = timesync('192.168.0.18')
        timesync3 = timesync('192.168.0.31')
        timesync4 = timesync('192.168.0.19')

        piOneBitrate = timesync1.raspiVidCommand.split("-b", 1)[1].split()[0]
        piTwoBitrate = timesync2.raspiVidCommand.split("-b", 1)[1].split()[0]
        piThreeBitrate = timesync3.raspiVidCommand.split("-b", 1)[1].split()[0]
        piFourBitrate = timesync4.raspiVidCommand.split("-b", 1)[1].split()[0]

        print "RPi 1 Bit Rate: " + piOneBitrate
        print "RPi 2 Bit Rate: " + piTwoBitrate
        print "RPi 3 Bit Rate: " + piThreeBitrate
        print "RPi 4 Bit Rate: " + piFourBitrate

        self.assertEqual(piOneBitrate, '25000000')
        self.assertEqual(piTwoBitrate, '25000000')
        self.assertEqual(piThreeBitrate, '25000000')
        self.assertEqual(piFourBitrate, '25000000')

if __name__ == '__main__':
    unittest.main()
