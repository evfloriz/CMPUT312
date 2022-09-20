#!/usr/bin/env python3

from movement import MoveHandler
from time import sleep

def line(robot):
    robot.drive(100, "forwards", 10)

def rotate(robot):
    robot.spin(360, "left", 10)

def main():
    # Open output file
    f = open("part2.out", "w")
    
    robot = MoveHandler()

    line(robot)
    #rotate(robot)

    # Write final position to file
    robot.write_pos_to_file(f)
    f.close()

    # Sleep so the user can read the screen output
    sleep(20)

main()
