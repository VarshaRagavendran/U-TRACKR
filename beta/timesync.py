import paramiko, sys

class timesync(object):

    def connect(self):
        target_host = '10.24.127.81'
        target_port = 22
        un = 'pi'
        pwd = 'raspberry'

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect( hostname = target_host , username = un, password = pwd ) 
        return ssh

    def getTimeStamp(self, ssh):
        stdin, stdout, stderr = ssh.exec_command('date \'+%Y-%m-%d %H:%M:%S.%N\'')
        return stdout.read()