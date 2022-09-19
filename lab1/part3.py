#!/usr/bin/env python3

from time import sleep
from movement import MoveHandler

def rectangle(robot, velocity):
    
    for i in range(4):
        robot.drive(10, "forwards", velocity)
        robot.spin(90, "left", velocity)
        
def lemniscate(robot, radius, velocity):
    
    robot.turn(360, radius, "left", velocity)
    robot.turn(360, radius, "right", velocity)
        
def line(robot, velocity):
    
    robot.drive(5, "forward", velocity)

def circle(robot, radius, velocity):
    
    robot.turn(360, radius, "left", velocity)

def main():
    
    robot = MoveHandler()
    
    rectangle(robot, 10)
    #lemniscate(robot, 5, 5)
    #line(robot, 5)
    #circle(robot, 5, 5)

main()