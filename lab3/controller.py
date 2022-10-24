#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

import time
from server import Server
from queue import Queue

class Controller:
    def __init__(self):
        self.host = "172.17.0.1"
        #host = "localhost"
        self.port = 9999
        self.server = Server(self.host, self.port)
        self.queue = Queue()

        

    def sendAngles(self):
        i = 0
        while i < 3:
            self.server.sendAngles(20, 20, self.queue)
            i += 1
            response = self.queue.get()
            print("Received: " + response)

        self.server.sendTermination()
        #response = queue.get()
        #print(response)
        print("Exiting server")
        time.sleep(1)


def main():
    controller = Controller()
    controller.sendAngles()

main()

        

