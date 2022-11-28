#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

from time import sleep
from color_tracking import Tracker
from server import Server
from queue import Queue

connect = True

class Controller:
    
    def __init__(self):
        self.tracker = Tracker('b', 'r')

        if (connect):
            host = "172.17.0.1"
            port = 9999
            self.server = Server(host, port)

        self.queue = Queue()

    def sendSpeed(self, left_speed, right_speed):
        print(left_speed)
        print(right_speed)
        self.server.sendSpeed(left_speed, right_speed, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def track(self):
        while (True):
            print(self.tracker.point)
            print(self.tracker.goal)
            self.sendSpeed(10, 10)
            sleep(1)


def main():
    controller = Controller()
    
    controller.track()
    

main()

        
