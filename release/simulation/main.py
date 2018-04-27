from threading import Thread
from simulation import simulation
import time

simulator = simulation()

def func1():
	while True:
		simulator.setCoordinates(5.5,2.2,3.3)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(13.4,5.5,2.2)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(9.5,4.4,0.3)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(10.3,9.2,4.5)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(1,0.1,0.1)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(0.8,4,5.4)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(11.6,7.4,6.1)
		simulator.simulate()
		time.sleep(5)
		simulator.setCoordinates(3.9,5.3,2.3)
		simulator.simulate()
		time.sleep(5)

if __name__=='__main__':
    func1()
