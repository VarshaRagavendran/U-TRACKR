import paramiko, sys

class timesync(object):

    def __init__(self, ip):
        target_host = ip
        target_port = 22
        un = 'pi'
        pwd = 'raspberry'

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect( hostname = target_host , username = un, password = pwd ) 

    def runRaspiVid(self):
        stdin, stdout, stderr = self.ssh.exec_command('raspivid -t 0 -n -w 1280 -h 720 -fps 30 -ex fixedfps -b 25000000 -vf -o - | nc -l 5000')
        return stdout.read()

    def getTimeStamp(self):
        stdin, stdout, stderr = self.ssh.exec_command('date \'+%Y-%m-%d %H:%M:%S.%N\'')
        return stdout.read()