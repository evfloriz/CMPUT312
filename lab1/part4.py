#!/usr/bin/env python3

from time import sleep
from movement import MoveHandler

def deadReckoning(robot, commands, file):    
    for command in commands:
        robot.move(command[0], command[1], command[2])
        robot.write_state_to_file(file)
        sleep(1)

def main():

    # Open output file
    file = open("part4.out", "w")
    
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
    robot.write_state_to_file(file)
    file.close()

    # Sleep so the user can read the screen output
    sleep(20)
    
main()
