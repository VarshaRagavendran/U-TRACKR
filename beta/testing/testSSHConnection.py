import unittest
import time
from tracker import tracker
from timesync import timesync
from checker import checker
import psutil

class TestSSHConnection(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()