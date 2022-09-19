#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds

# Vehicle
axelLength = 

# Wheel (cm)
wheelDiameter = 5.6
wheelCircumference = 3.14159265359*wheelDiameter

# Motor (rotations per second)
motorRPS = 165/60

def drive(distance, direction, velocity):
    
    time = distance/velocity
    angularVelocity = velocity/(wheelDiameter/2)
    percent = angularVelocity/motorRPS
    
    if direction is "forwards":
    
        motor.on_for_seconds(left_speed = SpeedPercent(percent), right_speed = SpeedPercent(percent), seconds = time)
        
    elif direction is "backwards":
    
        motor.on_for_seconds(left_speed = -SpeedPercent(percent), right_speed = -SpeedPercent(percent), seconds = time)
    
def spin(degrees, direction, velocity):
    
    radians = degrees*(3.14159265359/180)
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
    
    leftPercent = leftAngularVelocity/motorRPS
    rightPercent = rightAngularVelocity/motorRPS
    motor.on_for_seconds(left_speed = SpeedPercent(leftPercent), right_speed = SpeedPercent(rightPercent), seconds = time)
        

def turn(degrees, turnRadius, direction, velocity):
    
    radians = degrees*(3.14159265359/180)
    distance = radians*turnRadius
    time = distance/velocity
    angularVelocity = radians/time
    angularVelocity = angularVelocity/(2*3.14159265359)
    
    if direction is "left":
        
        leftVelocity = (turnRadius-(axelLength/2))*angularVelocity
        rightVelocity = (turnRadius+(axelLength/2))*angularVelocity
        
    elif direction is "right":

        leftVelocity = (turnRadius+(axelLength/2))*angularVelocity
        rightVelocity = (turnRadius-(axelLength/2))*angularVelocity
        
    leftAngularVelocity = leftVelocity/(wheelDiameter/2)
    rightAngularVelocity = rightVelocity/(wheelDiameter/2)
    
    leftPercent = leftAngularVelocity/motorRPS
    rightPercent = rightAngularVelocity/motorRPS
    motor.on_for_seconds(left_speed = SpeedPercent(leftPercent), right_speed = SpeedPercent(rightPercent), seconds = time)
    
