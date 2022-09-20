#!/usr/bin/env python3

from math import cos, sqrt, radians
from time import sleep
from movement import MoveHandler

def rectangle(robot, distance, driveVelocity, spinVelocity):
    
    for i in range(4):
        robot.drive(distance, "forwards", driveVelocity)
        robot.spin(90, "left", spinVelocity)
        
def lemniscate(robot, radius, velocity):
    
    #distance = sqrt(2) * radius / cos(radians(45))
    #robot.turn(270, radius, "left", velocity)
    #robot.drive(distance, "forwards", velocity)
    #robot.turn(270, radius, "right", velocity)
    #robot.drive(distance, "forwards", velocity)
    
    distance = radius * (sqrt((1 - 2 * cos(radians(135))) / cos(radians(67.5))))
    robot.drive(distance, "forwards", velocity)
    robot.turn(225, radius, "left", velocity)
    robot.drive(distance, "forwards", velocity)
    robot.turn(225, radius, "right", velocity)
    
        
def line(robot, distance, velocity):
    
    robot.drive(distance, "forward", velocity)

def circle(robot, radius, velocity):
    
    robot.turn(360, radius, "left", velocity)

def main():
    
    robot = MoveHandler()
    
    #rectangle(robot, 20, 20, 5)
    lemniscate(robot, 20, 10)
    #line(robot, 20, 10)
    #circle(robot, 10, 10)

main()