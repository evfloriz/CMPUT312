#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Oct 5, 2022
 
Brick Number: g10

Lab Number: 2

Problem Number: 2
 
Brief Program/Problem Description: 

	Arm forward kinematics
    moveToAngle: move motors according to specified angles and write position to file
    distance: allow user to read in two positions by moving arm and pressing touch sensor,
    then calculate distance between those points
    angle: allow user to read in three positions by moving arm and pressing touch sensor,
    then calculate the angle created by the two lines with the intersection at the first point

Brief Solution Summary:
    See movement.py

Used Resources/Collaborators:
	See movement.py

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from math import atan, degrees, sqrt
from time import sleep
from movement import MoveHandler
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor
    
def moveToAngle(angle1, angle2):
    file = open("part2_move.out", "w")
    robot = MoveHandler(file)
    robot.anglePositionMove(angle1, angle2)
    file.close()


def distance():
    # Get positions from motor angles after two button presses
    # and calculate the distance between them.

    # Robot must start at angle 0, 0 (arm pointing straight
    # and to the right)
    
    file = open("part2_distance.out", "w")
    robot = MoveHandler(file)
    robot.readAngles(2)
    x_distance = abs(robot.x_coordinate[1]-robot.x_coordinate[2])
    y_distance = abs(robot.y_coordinate[1]-robot.y_coordinate[2])
    distance = sqrt(x_distance**2 + y_distance**2)
    robot.file.write("Distance: " + str(distance) + "\n")
    file.close()
    
def angle():
    # Get positions from motor angles after three button presses
    # and compute the angle of the lines formed by points 1 and 2
    # and points 1 and 3, with point 1 being their intersection.

    # Robot must start at angle 0, 0 (arm pointing straight
    # and to the right)
    
    points_x = []
    points_y = []

    file = open("part2_angle.out", "w")
    robot = MoveHandler(file)
    robot.readAngles(3)
    points_x.append(robot.x_coordinate[1])
    points_y.append(robot.y_coordinate[1])
    points_x.append(robot.x_coordinate[2] - points_x[0])
    points_y.append(robot.y_coordinate[2] - points_y[0])
    points_x.append(robot.x_coordinate[3] - points_x[0])
    points_y.append(robot.y_coordinate[3] - points_y[0])
    
    angle1 = degrees(atan(points_y[1]/points_x[1]))
    angle2 = degrees(atan(points_y[2]/points_x[2]))
    
    if points_x[1] < 0:   
        
        angle1 = 180 + angle1
    
    if points_x[2] < 0:
        
        angle2 = 180 + angle2

    difference = abs(angle1 - angle2)
    
    robot.file.write("Angle: " + str(difference) + "\n")
    file.close()
    
def main():

    #distance()
    #angle()
    moveToAngle(45, 90)

main()