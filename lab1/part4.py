#!/usr/bin/env python3

from time import sleep
from movement import MoveHandler

def deadReckoning(robot, commands):
    f = open("part4.out", "w")
    
    final_odom = {"x": 0, "y": 0, "theta": 0}
    for command in commands:
        odom = robot.move(command[0], command[1], command[2])
        f.write(str(odom) + "\n")
        
        final_odom["x"] += odom["x"]
        final_odom["y"] += odom["y"]
        final_odom["theta"] += odom["theta"]
        sleep(1)
        
    f.write(str(final_odom) + "\n")
    f.close()
    
    # Sleep so the user can read the screen output
    sleep(20)

def main():
    
    robot = MoveHandler()
    
    # Left motor speed, right motor speed, seconds
    commands = [
        [ 80, 60, 2 ],
        [ 60, 60, 1 ],
        [ -50, 80, 2 ]
    ]
    
    deadReckoning(robot, commands)
    
main()