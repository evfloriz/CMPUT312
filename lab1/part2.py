#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Sept 21, 2022
 
Brick Number: g10

Lab Number: 1

Problem Number: 2
 
Brief Program/Problem Description: 

	Testing error gathering methods for straight lines and rotations

Brief Solution Summary:

	Use movement interface to move in a straight line and rotate

Used Resources/Collaborators:
	See movement.py

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from movement import MoveHandler
from time import sleep

def line(robot):
    distance = 50
    velocity = 30

    robot.drive(distance, "forwards", velocity)

def rotate(robot):
    degrees = 360
    velocity = 30

    robot.spin(degrees, "left", velocity)

def main():
    # Open output file
    file = open("part2.out", "w")
    
    robot = MoveHandler(file)    
    
    #line(robot)
    rotate(robot)

    # Close output file
    file.close()

main()
