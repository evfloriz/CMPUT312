#!/usr/bin/env python3

from math import cos, sqrt, radians
from time import sleep
from movement import MoveHandler

def rectangle(robot, distance, driveVelocity, spinVelocity, direction):
    
    # Move forward and spin in place right angle four times based on input
    for i in range(4):
        robot.drive(distance, "forwards", driveVelocity)
        robot.spin(90, direction, spinVelocity)
        
def lemniscate(robot, radius, velocity):
    
    #distance = sqrt(2) * radius / cos(radians(45))
    #robot.turn(270, radius, "left", velocity)
    #robot.drive(distance, "forwards", velocity)
    #robot.turn(270, radius, "right", velocity)
    #robot.drive(distance, "forwards", velocity)
    
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
    
    rectangle(robot, 20, 10, 10, "left")
    #lemniscate(robot, 10, 10)
    #line(robot, 20, 10)
    #circle(robot, 10, 10)

    # Close output file
    file.close()

main()
