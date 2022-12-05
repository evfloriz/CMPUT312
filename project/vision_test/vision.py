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
        print(self.tracker)

        if (connect):
            host = "172.17.0.1"
            port = 9999
            self.server = Server(host, port)
            self.queue = Queue()

    def __del__(self):
        self.server.close()

    def sendCoords(self, coords):
        print(coords)
        self.server.sendCoords(coords, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def track(self):
        while (True):
            print(self.tracker.point)
            print(self.tracker.goal)

            if (connect):
                self.sendCoords(self.tracker.point[0])
            
            sleep(1)


def main():
    controller = Controller()
    
    controller.track()
    

main()

        
