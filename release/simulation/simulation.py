from threading import Thread
import random
import socket
import json
import random
import time

class simulation(object):

  def __init__(self):
      self.host = 'localhost'
      self.port = 50004
      self.backlog = 5
      self.size = 1025
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.s.bind((self.host,self.port)) 
      self.s.listen(self.backlog) 
      self.client, self.address = self.s.accept() 

  def toString(self):
      return str(self.x)+","+str(self.y)+","+str(self.z)+ "\r\n"

  def simulate(self):
      print str(self.x)+","+str(self.y)+","+str(self.z)+ "\r\n"
      #time.sleep(5)
      print "Client connected."
      self.client.send(str(self.x)+","+str(self.y)+","+str(self.z)+ "\r\n")

  def setCoordinates(self, x, y, z):
    print "X" + str(x)
    self.x = x
    self.y = y
    self.z = z
