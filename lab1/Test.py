#!/usr/bin/env python3

from time import sleep
from math import pi

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds

# Axel (cm)
axelLength = 10.5

# Wheel (cm)
wheelDiameter = 5.6
wheelCircumference = 3.14159265*wheelDiameter

# Motor (rotations per second)
motorRPS = 165/60
    
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

def spin(degrees, direction, velocity):
    
    radians = degrees*(3.14159265/180)
    distance = radians*(axelLength/2)
    time = distance/velocity
    
    if direction is "left":
        
        leftVelocity = -velocity
        rightVelocity = velocity
        
    elif direction is "right":

        leftVelocity = velocity
        rightVelocity = -velocity
        
    leftAngularVelocity = leftVelocity/(wheelDiameter/2)
    rightAngularVelocity = rightVelocity/(wheelDiameter/2)
    
    leftPercent = leftAngularVelocity*100/(2*pi)/motorRPS
    rightPercent = rightAngularVelocity*100/(2*pi)/motorRPS
    tank_drive.on_for_seconds(SpeedPercent(leftPercent), SpeedPercent(rightPercent), time)
    
def turn(degrees, turnRadius, direction, velocity):
    
    radians = degrees*(3.14159265/180)
    distance = radians*turnRadius
    time = distance/velocity
    angularVelocity = radians/time
    angularVelocity = angularVelocity/(2*3.14159265)
    
    if direction is "left":
        
        leftVelocity = (turnRadius-(axelLength/2))*angularVelocity
        rightVelocity = (turnRadius+(axelLength/2))*angularVelocity
        
    elif direction is "right":

        leftVelocity = (turnRadius+(axelLength/2))*angularVelocity
        rightVelocity = (turnRadius-(axelLength/2))*angularVelocity
        
    leftAngularVelocity = leftVelocity/(wheelDiameter/2)
    rightAngularVelocity = rightVelocity/(wheelDiameter/2)
    
    leftPercent = leftAngularVelocity*100/motorRPS
    rightPercent = rightAngularVelocity*100/motorRPS
    tank_drive.on_for_seconds(SpeedPercent(leftPercent), SpeedPercent(rightPercent), time)
    
    
#turn(360, 10, "left", 10)
#turn(360, 10, "right", 10)
for i in range(4):
    robot.drive(5, "forward", velocity)
    robot.spin(90, "left", velocity)

