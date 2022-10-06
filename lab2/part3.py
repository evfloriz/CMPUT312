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

def midpoint(input):
    
    file = open("midpoint.out", "w")
    robot = MoveHandler(file)
    robot.angleCoordinate()
    x_midpoint = abs(robot.x_coordinate[1]-robot.x_coordinate[2])/2
    y_midpoint = abs(robot.y_coordinate[1]-robot.y_coordinate[2])/2
    
    if input is "Analytic":
        robot.positionAnalytic(x_midpoint,y_midpoint)
    elif input is "Numerical":
        robot.positionNumerical(x_midpoint,y_midpoint)
    
    robot.file.write("Distance: " + str(distance) + "\n")
    file.close()

def main():
    # Open output file
    file = open("part3.out", "w")

    # Construct robot object
    robot = MoveHandler(file)

    #robot.positionAnalytic(8.5, 16.0)
    robot.positionNumerical(8.5, 16.0)
    #robot.forwardKinematics(0, 0)

    # Close output file
    file.close()

main()

# change granularity to see when jacobian works and when inaccurate
# accuracy vs repeatability
