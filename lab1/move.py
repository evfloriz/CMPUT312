#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

def move(input):
    
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
    
    if input is "rectangle":
        
        for i in range(4):
            tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 10)
            tank_drive.turn_right(SpeedPercent(5), 90)
        
    elif input is "lemniscate":
        
        tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 10)

    elif input is "straight":
        
        tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 10)
        
    elif input is "circle":
    
        tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 10)
    
move("rectangle")