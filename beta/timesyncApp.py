from timesync import timesync

t = timesync('192.168.1.248')
while True:
    print t.getTimeStamp()