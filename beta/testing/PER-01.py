import unittest
import time
import sys
sys.path.append("..")
import tracker
import timesync
import checker
import psutil

class testCPUUsage(unittest.TestCase):

    #PER-01
    def testCPUUsage(self):
        timesync1 = timesync('192.168.0.21')
        stdin1, stdout1, stderr1 = timesync1.ssh.exec_command('./cpuUsage.sh')
        self.assertLess(stdout1.read().rstrip(), 100)

if __name__ == '__main__':
    unittest.main()
