#!/usr/bin/env python3

'''
Group Members: Evan Florizone, Yiyan Zhang

Date: Oct 26, 2022
 
Brick Number: g10

Lab Number: 3

Problem Number: 1 and 2
 
Brief Program/Problem Description: 
    Handle client-side code for robot. Turn angles sent from server into motion.

Brief Solution Summary:
    getAnglesFromServer - poll for data from the server and move to the
    specified angle until the exit code is sent. After moving to the specified
    angle the done code is sent so the server knows it can send the next angle.
    moveToAngle - move to the specified angles. Brake is set to false to the
    arm follows a more fluid motion, and block is set to false so both motors
    can start to move at the same time. After both motors are moving, it waits
    until both motors have stopped before moving on.

Used Resources/Collaborators:
    client.py
	
I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
'''

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
import time
from client import Client

class Robot:
    def __init__(self):
        host = "142.244.173.149"
        #host = "172.17.0.1"
        port = 9999
        self.client = Client(host, port)

        # Motor data
        self.motor1 = LargeMotor(OUTPUT_A)
        self.motor2 = LargeMotor(OUTPUT_B)
        self.motor1_dir = -1        # motor1 direction is flipped
        self.motor2_dir = 1

        self.speed = SpeedPercent(5)

        self.file = open("robot.out", "w")

    def __del__(self):
        self.client.close()
        self.file.close()

    def getAnglesFromServer(self):
        while True:
            # Receive data from server
            data = self.client.pollData().split(',')
            print(data)
            if (data[0] == "EXIT"):
                break
            
            # Move to angle sent by server
            self.moveToAngle(float(data[0]), float(data[1]))

            # Send done
            self.client.sendDone()

        self.file.write("Exiting client\n")


    def moveToAngle(self, base_angle, joint_angle):
        self.file.write("Moving to " + str(base_angle) + ", " + str(joint_angle) + "\n")
        motor1_degrees = base_angle * self.motor1_dir
        motor2_degrees = joint_angle * self.motor2_dir
        self.motor1.on_for_degrees(self.speed, motor1_degrees, brake=False, block=False)
        self.motor2.on_for_degrees(self.speed, motor2_degrees, brake=False, block=False)
        self.motor1.wait_until_not_moving()
        self.motor2.wait_until_not_moving()


def main():
    robot = Robot()
    robot.getAnglesFromServer()

main()