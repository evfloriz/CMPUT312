#!/usr/bin/env python3

from time import sleep
from movement import MoveHandler

def deadReckoning(robot, commands):    
    for command in commands:
        robot.move(command[0], command[1], command[2])
        sleep(1)

def main():

    # Open output file
    f = open("part4.out", "w")
    
    # Construct robot object
    robot = MoveHandler()
    
    # Left motor speed, right motor speed, seconds
    commands = [
        [ 30, 50, 2 ],
        [ 60, 60, 1 ]
        #[ -50, 80, 2 ]
    ]
    
    deadReckoning(robot, commands)

    # Write final position to file
    robot.write_pos_to_file(f)
    f.close()

    # Sleep so the user can read the screen output
    sleep(20)
    
main()
