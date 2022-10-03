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

from math import degrees, radians, pi, sin, cos, acos, asin, atan2, sqrt
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent

from time import sleep

import mtx

class MoveHandler:

    def __init__(self, file):
        self.file = file

        #self.motor1 = LargeMotor(OUTPUT_A)
        #self.motor2 = LargeMotor(OUTPUT_B)

        self.motor1_dir = 1
        self.motor2_dir = -1        # motor2 direction is flipped

        self.speed = SpeedPercent(10)

        # Length of link 1 and 2 in cm
        self.l1 = 16.0
        self.l2 = 8.5

        self.granularity = 50

        self.current_pos = [0.0, 24.5]
    
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
        # J(r) * dr = W - f(r)
        # r = r + dr
        #
        # r = vector of angles, initially guessed and then iterated
        # J(r) = Jacobian of f wrt r
        # dr = rk+1 - rk
        # W = point we want to go to
        # f(r) = evaluated point given our guess/iterated angle

        # Points along trajectory
        # trajectory = current pos - desired pos
        # step = trajectory / granularity
        # repeat granularity times

        angles = [pi / 2, 0.1]            # x angle is 90 from 0
        init_pos = self.current_pos

        step = [x - init_pos[0], y - init_pos[1]]
        step[0] /= self.granularity
        step[1] /= self.granularity

        self.file.write("part3 test\n")

        for i in range(self.granularity):
            # Compute LHS of equation with current angles guess
            goal = [init_pos[0] + i * step[0], init_pos[1] + i * step[1]]        # current goal is one more step length away from initial
            guess = self.forwardKinematics(angles)
            lhs = [goal[0] - guess[0], goal[1] - guess[1]]

            # Compute Jacobian with current angles guess
            J = self.computeJacobian(angles)         

            # Solve to converge angles guess toward a solution
            delta_angles = mtx.solve(mtx.lu(J), lhs)

            angles[0] += delta_angles[0]
            angles[1] += delta_angles[1]

            # Move motors towards the improved guess
            motor1_degrees = self.motor1_dir * degrees(delta_angles[0])
            motor2_degrees = self.motor2_dir * degrees(delta_angles[1])

            #self.motor1.on_for_degrees(self.speed, motor1_degrees)
            #self.motor2.on_for_degrees(self.speed, motor2_degrees)

            # Write state for debugging
            self.file.write("goal: " + str(goal) + "\n" +
                            "guess: " + str(guess) + "\n" +
                            "lhs: " + str(lhs) + "\n" +
                            "angles: " + str(angles) + "\n" +
                            "motor degrees 1: " + str(motor1_degrees) + "\n" +
                            "motor degrees 2: " + str(motor2_degrees) + "\n" +
                            "-------------------\n")

            #sleep(1.0)


    def forwardKinematics(self, angles):
        # Return current x and y of end effector given joint angles (in radians)
        posX = self.l2 * cos(angles[0] + angles[1]) + self.l1 * cos(angles[0])
        posY = self.l2 * sin(angles[0] + angles[1]) + self.l1 * sin(angles[0])

        #self.current_pos[0] = posX
        #self.current_pos[1] = posY
        
        #self.write_pos_to_file()
        
        return [posX, posY]

    def computeJacobian(self, angles):
        a = -self.l2 * sin(angles[0] + angles[1]) - self.l1 * sin(angles[0])
        b = -self.l2 * sin(angles[0] + angles[1])

        c = self.l2 * cos(angles[0] + angles[1]) + self.l1 * cos(angles[0])
        d = self.l2 * cos(angles[0] + angles[1])

        J = [[a, b],
            [c, d]]

        return J

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

    def write_pos_to_file(self):
        self.file.write("x: " + self.current_pos[0] + "\n" +
                        "y: " + self.current_pos[1] + "\n")


