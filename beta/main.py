import threading
from threading import Thread
from tracker import tracker

utrackr = tracker('192.168.0.33')
# utrackr.hsvModifier()
# utrackr.tracker()

def func1():
	utrackr.printTimeStamp()

def func2():
	utrackr.tracker()

if __name__=='__main__':
	Thread(target = func1).start()
	Thread(target = func2).start()

# utrackr.stopTracker()