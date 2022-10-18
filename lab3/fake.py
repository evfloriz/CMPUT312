#!/usr/bin/env python3

#from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
import time
from client import Client

class Robot:
    def __init__(self):
        host = "172.17.0.1"
        #host = "localhost"
        port = 9999
        self.client = Client(host, port)

        # Motor data
        #self.motor1 = LargeMotor(OUTPUT_A)
        #self.motor2 = LargeMotor(OUTPUT_B)
        #self.motor1_dir = -1        # motor1 direction is flipped
        #self.motor2_dir = 1

        #self.speed = SpeedPercent(10)

    def getAnglesFromServer(self):
        while True:
            # Receive data from server
            data = self.client.pollData().split(',')
            print(data)
            if (data[0] == "EXIT"):
                break
            
            # Move to angle sent by server
            #self.moveToAngle(float(data[0]), float(data[1]))
            time.sleep(3)

            # Send done
            self.client.sendDone()
            time.sleep(1)

        print("Exiting client")


    def moveToAngle(self, base_angle, joint_angle):
        print("moving to " + str(base_angle) + " " + str(joint_angle))
        motor1_degrees = base_angle * self.motor1_dir
        motor2_degrees = joint_angle * self.motor2_dir
        self.motor1.on_for_degrees(self.speed, motor1_degrees)
        self.motor2.on_for_degrees(self.speed, motor2_degrees)


            


def main():
    robot = Robot()
    robot.getAnglesFromServer()
    time.sleep(10)


main()