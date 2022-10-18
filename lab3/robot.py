#!/usr/bin/env python3

#from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
import time
from client import Client

class Robot:
    def __init__(self):
        #host = "172.17.0.1"
        host = "localhost"
        port = 9999
        self.client = Client(host, port)

        while True:
            data = self.client.pollData().split(',')
            print(data)
            if (data[0] == "EXIT"):
                break
            # move
            print("moving")
            time.sleep(2)
            self.client.sendDone()
            time.sleep(1)

        print("Exiting client")
            


def main():
    robot = Robot()


main()