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
    # Get positions from motor angles after two button presses
    # and calculate midpoint, then move arm to that position
    
    # Robot must start at angle 0, 0 (arm pointing straight
    # and to the right)
    
    file = open("part3_midpoint.out", "w")
    robot = MoveHandler(file)
    robot.readAngles(2)
    x_midpoint = abs(robot.x_coordinate[1]-robot.x_coordinate[2])/2
    y_midpoint = abs(robot.y_coordinate[1]-robot.y_coordinate[2])/2

    # Set inverse kinematics start point to robot's current position
    robot.update_ik_start()

    robot.file.write("Moving to point (" + str(x_midpoint) + ", " +
                        str(y_midpoint) + ")\n")
    
    if input is "Analytical":
        robot.positionAnalytic(x_midpoint,y_midpoint)
    elif input is "Numerical":
        robot.positionNumerical(x_midpoint,y_midpoint)
    
    file.close()

def position(input, x, y):
    # Open output file
    file = open("part3_position.out", "w")

    # Construct robot object
    robot = MoveHandler(file)

    if input is "Analytical":
        robot.positionAnalytic(x, y)
    elif input is "Numerical":
        robot.positionNumerical(x, y)

    # Close output file
    file.close()

def main():
    
    #position("Analytical", 8.5, 16)
    #position("Numerical", 12, 12)

    midpoint("Numerical")

main()



# change granularity to see when jacobian works and when inaccurate
# accuracy vs repeatability
