#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Oct 5, 2022
 
Brick Number: g10

Lab Number: 2

Problem Number: 3
 
Brief Program/Problem Description: 

	Implement a movement class to handle common movement functions.

Brief Solution Summary:

    Other helper functions are implemented to facilitate this core functionality

Used Resources/Collaborators:
	ev3dev API,
    ev3dev tutorial https://sites.google.com/site/ev3python/learn_ev3_python

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from math import degrees, radians, pi, sin, acos, asin, atan2, sqrt
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent

class MoveHandler:

    def __init__(self, file):
        self.file = file

        self.motor1 = LargeMotor(OUTPUT_A)
        self.motor2 = LargeMotor(OUTPUT_B)

        self.motor1_dir = 1
        self.motor2_dir = -1        # motor2 direction is flipped

        self.speed = SpeedPercent(10)

        # Length of link 1 and 2 in cm
        self.l1 = 16.0
        self.l2 = 8.5

        self.start_pos = [0.0, 24.5]
        
    def positionAnalytic(self, x, y):
        # Calculate motor angles geometrically
        # See report for derivation
        theta2 = acos((x**2 + (y**2) - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2))
        theta1 = asin((self.l2 * sin(theta2)) / sqrt(x**2 + y**2)) + atan2(y, x)

        self.file.write("theta1: " + str(theta1) + " theta2: " + str(theta2) + "\n")
        self.file.write("theta1 deg: " + str(90 - degrees(theta1)) + " theta2 deg: " + str(degrees(theta2)) + "\n")

        motor1_degrees = self.motor1_dir * (90 - degrees(theta1))
        motor2_degrees = self.motor2_dir * degrees(theta2)

        self.motor1.on_for_degrees(self.speed, motor1_degrees)
        self.motor2.on_for_degrees(self.speed, motor2_degrees)

        self.write_angle_to_file()

    def positionNumerical(self, x, y):
        # Using Newton's method
        pass

    def midpoint(self, x1, y1, x2, y2):
        # wait until button is pressed
        # read angles
        # put through forward kinematics to find pos1
        # wait until button is pressed
        # read angles
        # put through forward kinematics to find pos2
        # calculate midpoint
        # use ik to find new angles
        # use current angles and new angles to find relative angles
        # move to position
        pass

    def write_angle_to_file(self):
        self.file.write("theta1: " + self.motor1.position + "\n" +
                        "theta2: " + self.motor2.position + "\n")


