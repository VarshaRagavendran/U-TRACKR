import unittest
import time
import sys
sys.path.append("..")
from tracker import tracker
from timesync import timesync
from checker import checker

class testCPUUsage(unittest.TestCase):

    #PER-01
    def testCPUUsage(self):
        timesync2 = timesync('192.168.0.18')
        timesync4 = timesync('192.168.0.19')
        timesync3 = timesync('192.168.0.31')
        timesync1 = timesync('192.168.0.21')
        stdin1, stdout1, stderr1 = timesync1.ssh.exec_command('./cpuUsage.sh')
        stdin2, stdout2, stderr2 = timesync2.ssh.exec_command('./cpuUsage.sh')
        stdin3, stdout3, stderr3 = timesync3.ssh.exec_command('./cpuUsage.sh')
        stdin4, stdout4, stderr4 = timesync4.ssh.exec_command('./cpuUsage.sh')
        rpiOneCpuUsage = int(stdout1.read().rstrip())
        rpiTwoCpuUsage = int(stdout2.read().rstrip())
        rpiThreeCpuUsage = int(stdout3.read().rstrip())
        rpiFourCpuUsage = int(stdout4.read().rstrip())
        print "RPi 1 CPU Usage: " + str(rpiOneCpuUsage)
        print "RPi 2 CPU Usage: " + str(rpiTwoCpuUsage)
        print "RPi 3 CPU Usage: " + str(rpiThreeCpuUsage)
        print "RPi 4 CPU Usage: " + str(rpiFourCpuUsage)
        self.assertLess(rpiOneCpuUsage, '100')
        self.assertLess(rpiTwoCpuUsage, '100')
        self.assertLess(rpiThreeCpuUsage, '100')
        self.assertLess(rpiFourCpuUsage, '100')

if __name__ == '__main__':
    unittest.main()
