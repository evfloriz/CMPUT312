#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

import time
from tracemalloc import start
from server import Server
from color_tracking import Tracker
from queue import Queue
from math import sin, asin, acos, atan2, degrees, sqrt

class Controller:
    def __init__(self):
        self.host = "172.17.0.1"
        #host = "localhost"
        self.port = 9999
        #self.server = Server(self.host, self.port)
        self.queue = Queue()

        # Length of link 1 and 2 in cm
        self.l1 = 16.0
        self.l2 = 8.5
        

    def sendAngles(self, motor1_degrees, motor2_degrees):
        self.server.sendAngles(motor1_degrees, motor2_degrees, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def track(self):
        print("Tracker Setup")
        tracker = Tracker('g', 'r')
        print("Moving on")
        while True:
            print("Point is at: "+str(tracker.point))
            print("Goal is at: "+str(tracker.goal))
            time.sleep(2)


    def exit(self):
        self.server.sendTermination()
        print("Exiting server")
        time.sleep(1)


def main():
    controller = Controller()
    
    controller.track()
    
    controller.exit()

main()

        

