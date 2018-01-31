import paramiko, sys

target_host = '10.24.127.81'
target_port = 22
un = 'pi'
pwd = 'raspberry'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = target_host , username = un, password = pwd ) 
stdin, stdout, stderr = ssh.exec_command('echo hello world')
print "STDOUT:\n%s\n\nSTDERR:\n%s\n" %( stdout.read(), stderr.read() )