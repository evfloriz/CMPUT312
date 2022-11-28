#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedPercent
import time
from client import Client

class Robot:
    def __init__(self):
        host = "172.17.0.1"
        port = 9999
        self.client = Client(host, port)

        # Motor data
        self.motor1 = LargeMotor(OUTPUT_D)
        self.motor2 = LargeMotor(OUTPUT_C)
        self.dir = -1

        self.seconds = 0.5

        self.file = open("robot.out", "w")

    def __del__(self):
        self.client.close()
        self.file.close()

    def getSpeedFromServer(self):
        while True:
            # Receive data from server
            data = self.client.pollData().split(',')
            print(data)
            if (data[0] == "EXIT"):
                break
            
            # Move to angle sent by server
            self.move(float(data[0]), float(data[1]))

            # Send done
            self.client.sendDone()

        self.file.write("Exiting client\n")


    def move(self, left_speed, right_speed):
        self.file.write("Moving at L: " + str(left_speed) + ", R:" + str(right_speed) + "\n")
        left_motor_speed = left_speed * self.dir
        right_motor_speed = right_speed * self.dir
        self.motor1.on_for_seconds(SpeedPercent(left_motor_speed), self.seconds, brake=True, block=False)
        self.motor2.on_for_seconds(SpeedPercent(right_motor_speed), self.seconds, brake=True, block=True)
        


def main():
    robot = Robot()
    robot.getSpeedFromServer()

main()