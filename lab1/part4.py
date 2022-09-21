#!/usr/bin/env python3

from time import sleep
from movement import MoveHandler

def deadReckoning(robot, commands, file):    
    for command in commands:
        robot.move(command[0], command[1], command[2])
        sleep(1)

def main():

    # Open output file
    file = open("part4.out", "w")
    
    # Construct robot object
    robot = MoveHandler(file)
    
    # Left motor speed, right motor speed, seconds
    commands = [
        [ 80, 60, 2 ],
        [ 60, 60, 1 ]
        [ -50, 80, 2 ]
    ]
    
    deadReckoning(robot, commands)

    # Close output file
    file.close()
    
main()
