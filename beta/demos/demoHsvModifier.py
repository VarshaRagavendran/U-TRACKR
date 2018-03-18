from threading import Thread
from tracker import tracker
from checker import checker
import time

# pi camera 1
utrackr = tracker('192.168.0.21')
utrackr.hsvModifier()
