from multiprocessing import Process
from tracker import tracker

utrackr = tracker('192.168.0.39')
#utrackr.hsvModifier()
utrackr.tracker()

# def func1():
# 	utrackr.printTimeStamp()

# def func2():
# 	utrackr.tracker()

# if __name__=='__main__':
# 	p1 = Process(target = func1)
# 	p1.start()
# 	p2 = Process(target = func2)
# 	p2.start()

# utrackr.stopTracker()