import unittest
import time
import sys
sys.path.append("..")
import tracker
import timesync
import checker
import psutil

class TestWifiConnection(unittest.TestCase):

    #FUNC-01
    def testWifiConnection(self):
        #init of timesync will establish sshconnection
        timesync2 = timesync('192.168.0.18')
        timesync4 = timesync('192.168.0.19')
        timesync3 = timesync('192.168.0.20')
        timesync1 = timesync('192.168.0.21')
        stdin1, stdout1, stderr1 = timesync1.ssh.exec_command('iwgetid -r')
        stdin2, stdout2, stderr2 = timesync2.ssh.exec_command('iwgetid -r')
        stdin3, stdout3, stderr3 = timesync3.ssh.exec_command('iwgetid -r')
        stdin4, stdout4, stderr4 = timesync4.ssh.exec_command('iwgetid -r')
        self.assertEquals(stdout1.read().rstrip(), stdout2.read().rstrip())
        self.assertEquals(stdout2.read().rstrip(), stdout3.read().rstrip())
        self.assertEquals(stdout3.read().rstrip(), stdout4.read().rstrip())
        #todo: check with computer's wifi


if __name__ == '__main__':
    unittest.main()
