from threading import Thread
from simulation import simulation
import random
import time

simulator = simulation()

def func1():
	while True:
		simulator.setCoordinates(random.uniform(0.0, 14.0),random.uniform(0.0, 14.0),random.uniform(0.0, 14.0))
		simulator.simulate()
		time.sleep(5)

if __name__=='__main__':
    func1()
