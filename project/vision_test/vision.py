#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

from time import sleep
from color_tracking import Tracker
from server import Server
from queue import Queue

connect = False

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
        self.server.sendTermination()
        self.server.close()

    def sendCoords(self, coords):
        print(coords)
        self.server.sendCoords(coords, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def track(self):
        while (True):
            print(self.tracker.point)

            if (connect):
                self.sendCoords(self.tracker.point[0])
            
            # What's the maximum rate? Is it possible to interpolate?
            sleep(0.1)


def main():
    controller = Controller()
    
    controller.track()
    

main()

        
