#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Sept 21, 2022
 
Brick Number: g10

Lab Number: 1

Problem Number: 5
 
Brief Program/Problem Description: 

	Implement a Braitenberg vehicle

Brief Solution Summary:

	Aggression - more power to left motor when left light sensor detects light,
    more power to right motor when right light sensor detects light.

    Cowardice - more power to right motor when left light sensor detects light,
    more power to left motor when right light sensor detects light.

Used Resources/Collaborators:
	In class discussion of Braitenberg vehicles

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from time import sleep

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

class Braitenberg:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        #self.move = MoveSteering(OUTPUT_A, OUTPUT_B)        # need to flip motors to drive forward
        self.dir = -1
        
        self.cs1 = ColorSensor(INPUT_3)       # right sensor
        self.cs2 = ColorSensor(INPUT_4)       # left sensor
        
        self.cs1.mode = 'COL-AMBIENT'
        self.cs2.mode = 'COL-AMBIENT'

        self.rate = 0.1

    def aggression(self):
        # Move towards light
        self.left_speed = self.cs1.value() * 2 * self.dir
        self.right_speed = self.cs2.value() * 2 * self.dir

    def cowardice(self):
        # Charge toward light if straight ahead, otherwise move away
        self.left_speed = self.cs2.value() * 2 * self.dir
        self.right_speed = self.cs1.value() * 2 * self.dir

    def love(self):
        # Untested
        # Non linear, move slow if dark or bright, move fast if medium
        self.left_speed = (self.cs1.value() / 5 - 20) ** 2 * self.dir
        self.right_speed = (self.cs2.value() / 5 - 20) ** 2 * self.dir

    def run(self):
        #behaviour = self.aggression
        behaviour = self.cowardice
        
        while(True):
            behaviour()
            
            self.tank_drive.on(SpeedPercent(self.left_speed), SpeedPercent(self.right_speed))
            sleep(self.rate)


def main():
    braitenberg = Braitenberg()
    braitenberg.run()

if __name__ == "__main__":
    main()
