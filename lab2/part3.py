#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Oct 5, 2022
 
Brick Number: g10

Lab Number: 2

Problem Number: 3
 
Brief Program/Problem Description: 

	Arm inverse kinematics, numerically and analytically

Brief Solution Summary:

Used Resources/Collaborators:
	See movement.py

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from movement import MoveHandler

def main():
    # Open output file
    file = open("part3.out", "w")

    # Construct robot object
    robot = MoveHandler(file)

    #robot.positionAnalytic(-10, 10)
    robot.positionNumerical(-10, 10)
    #robot.forwardKinematics(0, 0)

    # Close output file
    file.close()

main()
