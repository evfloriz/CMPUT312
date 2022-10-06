#!/usr/bin/env python3

from math import atan, degrees, sqrt
from time import sleep
from movement import MoveHandler
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import TouchSensor
    
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

    angle()

main()