from threading import Thread
import random
import socket
import json
import random
import time

host = 'localhost'
port = 50004
backlog = 5
size = 1025
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 

def toString(x,y,z):
    return str(x)+","+str(y)+","+str(z)+ " "

def simulatation(x,y,z):
    while 1:
      client, address = s.accept() 
      print "Client connected."
      while True:     
      	print toString(x,y,z)
      	#time.sleep(5)
        client.send(toString(x,y,z))
        break
      break       
      client.close()

#if __name__ == '__main__':
#    Thread(target = simulatation(5.5,2.2,3.3)).start()
    #Thread(target = simulatation(13.4,5.5,2.2)).start()
    #Thread(target = simulatation(9.5,4.4,0.3)).start()
    #Thread(target = simulatation(10.3,9.2,4.5)).start()


    #simulatation(13.4,5.5,2.2)
    #simulatation(9.5,4.4,0.3)
    #simulatation(10.3,9.2,4.5)


