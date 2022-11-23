#!/usr/bin/env python3

import util
import os
import sys
import time
import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor

# state constants
ON = True
OFF = False

def walk(fullStepSize, speed, leftHip, rightHip, leftAnkle, rightAnkle, l2, distance):
    # Calculate First step size and perform
    halfStep = fullStepSize/2
    firstAndLastStep(halfStep, speed, leftHip, leftAnkle, rightHip, rightAnkle, l2)
    
    #Add step length to total distance
    totalDistance = halfStep

    #Perform walking until we reach the desired distance
    while (distance - totalDistance) > 0:
        step(fullStepSize, speed, leftHip, rightHip, leftAnkle, rightAnkle, l2, distance)
        totalDistance += fullStepSize
    
    #Even out feet
    firstAndLastStep(halfStep, speed, leftHip, leftAnkle, rightHip, rightAnkle, l2)

    #Print total distance traveled
    util.debug_print("walked" + distance)
    
    return True

def firstAndLastStep(stepSize, speed, leftHip, leftAnkle, rightHip, rightAnkle, l2):
    #Take half step as first step with the right foot
    hipRotation = math.asin(stepSize/l2)
    leftAnkle.on_for_degrees(SpeedPercent(speed), -45)
    leftHip.on_for_degrees(SpeedPercent(speed), -math.degrees(hipRotation))
    rightHip.on_for_degrees(SpeedPercent(speed), math.degrees(hipRotation))
    leftAnkle.on_for_degrees(SpeedPercent(speed), 45)
    return True

def step(FullStepSize, speed, leftHip, rightHip, leftAnkle, rightAnkle, l2, distance):
    #Right foot step
    hipRotation = math.asin(FullStepSize/l2)
    leftAnkle.on_for_degrees(SpeedPercent(speed), -45)
    leftHip.on_for_degrees(SpeedPercent(speed), -math.degrees(hipRotation))
    rightHip.on_for_degrees(SpeedPercent(speed), math.degrees(hipRotation))
    leftAnkle.on_for_degrees(SpeedPercent(speed), 45) 

    #Left foot step
    hipRotation = math.asin(FullStepSize/l2)
    rightAnkle.on_for_degrees(SpeedPercent(speed), -45)
    rightHip.on_for_degrees(SpeedPercent(speed), -math.degrees(hipRotation))
    leftHip.on_for_degrees(SpeedPercent(speed), math.degrees(hipRotation))
    rightAnkle.on_for_degrees(SpeedPercent(speed), 45)

    return True