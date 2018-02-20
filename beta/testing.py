import unittest
import time
from tracker import tracker
from timesync import timesync
from checker import checker

class TestUTrackr(unittest.TestCase):

    #FUNC-01
    #def testWifiConnection(self):

    #FUNC-02
    def testSSHConnection(self):
        try:
            #init of timesync will establish sshconnection
            timesync2 = timesync('192.168.0.18')
            timesync4 = timesync('192.168.0.19')
            timesync3 = timesync('192.168.0.20')
            timesync1 = timesync('192.168.0.21')
        # possible exceptions thrown by paramiko api
        except AuthenticationException as e:
            self.fail('AuthenticationException raised', e)
        except SSHException as e:
            self.fail('SSHException raised', e)
        except BadHostKeyException as e:
            self.fail('BadHostKeyException raised', e)
        except socket.error as e:
            self.fail('Socket Error raised', e)
        else:
            pass

    #FUNC-03
    def test_sameTimeStamp(self):
        utrackr2 = tracker('192.168.0.18')
        utrackr4 = tracker('192.168.0.19')
        utrackr3 = tracker('192.168.0.20')
        utrackr = tracker('192.168.0.21')
        self.assertEquals(utrackr.timesync.getTimeStamp() ,utrackr2.timesync.getTimeStamp())
        self.assertEquals(utrackr2.timesync.getTimeStamp() ,utrackr3.timesync.getTimeStamp())
        self.assertEquals(utrackr3.timesync.getTimeStamp() ,utrackr4.timesync.getTimeStamp())

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

    #PER-01
    #def testCPUUsage(self):

    #PER-02
    #def testFPS(self):

    #PER-03
    #def testResolution(self):

    #PER-04
    #def testBitRate(self):

    #MTBF-01
    #def testMTBF(self):

    #COM-02
    #def testTrackMultipleObjects(self):


if __name__ == '__main__':
    unittest.main()
