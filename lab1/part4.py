#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Sept 21, 2022
 
Brick Number: g10

Lab Number: 1

Problem Number: 4
 
Brief Program/Problem Description: 

	Implement dead reckoning position controller

Brief Solution Summary:

	Use movement interface to move motors with power specified by commands list

Used Resources/Collaborators:
	See movement.py

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from time import sleep
from movement import MoveHandler
from ev3dev2.motor import SpeedPercent

def deadReckoning(robot, commands):    
    for command in commands:
        robot.move(SpeedPercent(command[0]), SpeedPercent(command[1]), command[2])
        sleep(1)

def main():

    # Open output file
    file = open("part4.out", "w")
    
    # Construct robot object
    robot = MoveHandler(file)
    
    # Left motor speed, right motor speed, seconds
    commands = [
        [ 80, 60, 2 ],
        [ 60, 60, 1 ],
        [ -50, 80, 2 ]
    ]
    
    deadReckoning(robot, commands)

    # Close output file
    file.close()
    
main()
