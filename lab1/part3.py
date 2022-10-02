#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Sept 21, 2022
 
Brick Number: g10

Lab Number: 1

Problem Number: 3
 
Brief Program/Problem Description: 

	Testing error when moving in a rectangle shape and a lemniscate.

Brief Solution Summary:

	Use movement interface to move in a rectangle 3 times and a lemniscate 3 times.

Used Resources/Collaborators:
	See movement.py

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from math import cos, sqrt, radians
from time import sleep
from movement import MoveHandler

def rectangle(robot, distance, driveVelocity, spinVelocity, direction):
    
    for i in range(3):
        # Move forward and spin in place right angle four times based on input
        for j in range(4):
            robot.drive(distance, "forwards", driveVelocity)
            robot.spin(90, direction, spinVelocity)
        
def lemniscate(robot, radius, velocity):
    
    #distance = sqrt(2) * radius / cos(radians(45))
    #robot.turn(270, radius, "left", velocity)
    #robot.drive(distance, "forwards", velocity)
    #robot.turn(270, radius, "right", velocity)
    #robot.drive(distance, "forwards", velocity)
    
    for i in range(3):
        # Move forward and turn angle based on input
        distance = radius * (sqrt((1 - 2 * cos(radians(135))) / cos(radians(67.5))))
        robot.drive(distance, "forwards", velocity)
        robot.turn(225, radius, "left", velocity)
        robot.drive(distance, "forwards", velocity)
        robot.turn(225, radius, "right", velocity)
    
        
def line(robot, distance, velocity):
    
    # Move forward based on input
    robot.drive(distance, "forward", velocity)

def circle(robot, radius, velocity):
    
    # Turn based on input
    robot.turn(360, radius, "left", velocity)

def main():
    # Open output file
    file = open("part3.out", "w")

    # Construct robot object
    robot = MoveHandler(file)
    
    #rectangle(robot, 20, 10, 5, "left")
    lemniscate(robot, 10, 10)
    #line(robot, 20, 10)
    #circle(robot, 10, 10)

    # Close output file
    file.close()

main()
