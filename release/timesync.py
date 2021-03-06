import paramiko, sys

class timesync(object):

    def __init__(self, ip):
        target_host = ip
        target_port = 22
        un = 'pi'
        pwd = 'raspberry'

        # self.raspiVidCommand = 'raspivid -t 0 -n -w 1280 -h 720 -fps 30 -rot 90 -ex fixedfps -ex auto -b 25000000 -o - | nc -l 5000'
        self.raspiVidCommand = 'raspivid -t 0 -n -w 640 -h 480 -fps 30 -rot 90 -ex fixedfps -ex auto -b 25000000 -o - | nc -l 5000'
        self.timeStampCommand = 'date \'+%Y-%m-%d %H:%M:%S\''
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect( hostname = target_host , username = un, password = pwd ) 

    def runRaspiVid(self):
        #<todo> raspivid command doesn't return anything to stdout. we need a way of knowing the command was successful or not
        stdin, stdout, stderr = self.ssh.exec_command(self.raspiVidCommand)

    def getTimeStamp(self):
        stdin, stdout, stderr = self.ssh.exec_command(self.timeStampCommand)
        # stdin, stdout, stderr = self.ssh.exec_command('date \'+%Y-%m-%d %H:%M:%S.%N\'')
        # stdin, stdout, stderr = self.ssh.exec_command('./timestamp.sh')
        # stdin, stdout, stderr = self.ssh.exec_command('while sleep 1; do echo \"$(date \'+%Y-%m-%d %H:%M:%S\')\"; done')
        return stdout.read().rstrip()

    def closeSSHClient(self):
        self.ssh.close()
        return True
