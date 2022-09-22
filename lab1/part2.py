#!/usr/bin/env python3

'''
Experiments

line:
3 trials at velocity = 10
    - 1 of 0.5m
    - 1 of 1.0m
    - 1 of 1.5m
3 trials at velocity = 20
    - 1 of 0.5m
    - 1 of 1.0m
    - 1 of 1.5m
3 trials at velocity = 40
    - 1 of 0.5m
    - 1 of 1.0m
    - 1 of 1.5m

rotate:
3 trials at velocity = 10
    - 1 of 360
    - 1 of 720
    - 1 of 1080
3 trials at velocity = 20
    - 1 of 360
    - 1 of 720
    - 1 of 1080
3 trials at velocity = 40
    - 1 of 360
    - 1 of 720
    - 1 of 1080

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
