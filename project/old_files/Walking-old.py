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
class Movement:

    def __init__(self, distance, speed, fullStepSize):
        self.distance = distance 
        self.speed = speed
        self.hip_width = 96 #mm
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)
        self.fullStepSize = fullStepSize
        

    def walk(self):
        # Calculate First step size and perform
        halfStep = self.fullStepSize/2
        self.firstAndLastStep(halfStep)
        
        #Add step length to total distance
        totalDistance = halfStep

        #Perform walking until we reach the desired distance
        while (self.distance - totalDistance) > 0:
            self.step(self.fullStepSize)
            totalDistance += self.fullStepSize
        
        #Even out feet
        self.firstAndLastStep(halfStep)

        #Print total distance traveled
        util.debug_print("walked" + self.distance)
        
        return True

    def firstAndLastStep(self, stepSize):
        #Take half step as first step with the right foot
        hipRotation = math.degrees(math.asin(stepSize/self.hip_width)) * 5
        # This multiplier in the hip rotation is to account for the 5-1 ratio of gears to motor
        
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        #Lift the right side up
        self.rightAnkle.on_for_degrees(self.speed, -220, brake=True, block=False)
        self.leftAnkle.on_for_degrees(self.speed, 110, brake=True, block=True)

        self.rightHip.on_for_degrees(self.speed, -hipRotation, brake=True, block=False)
        
        self.leftHip.on_for_degrees(self.speed, hipRotation, brake=True, block=True)

        self.leftAnkle.on_for_degrees(self.speed, 45)
        return True

    def step(self, fullStepSize):
        #Left foot full step
        hipRotation = math.degrees(math.asin(fullStepSize/self.hip_width)) * 5

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        
        self.leftAnkle.on_for_degrees(self.speed, -220, brake=True, block=False)
        self.rightAnkle.on_for_degrees(self.speed, 110, brake=True, block=True)

        self.rightHip.on_for_degrees(self.speed, -hipRotation, brake=True, block=False)
        self.leftHip.on_for_degrees(self.speed, hipRotation, brake=True, block=True)
        
        self.rightAnkle.on_for_degrees(self.speed, -110, brake=True, block=False)
        self.leftAnkle.on_for_degrees(self.speed, 220, brake=True, block=True) 

        #Right foot full step
        self.rightAnkle.on_for_degrees(self.speed, -220, brake=True, block=False)
        self.leftAnkle.on_for_degrees(self.speed, 110, brake=True, block=True)

        self.rightHip.on_for_degrees(self.speed, hipRotation, brake=True, block=False)
        self.leftHip.on_for_degrees(self.speed, -hipRotation, brake=True, block=True)


        self.rightAnkle.on_for_degrees(self.speed, -110, brake=True, block=False)
        self.leftAnkle.on_for_degrees(self.speed, 220, brake=True, block=True)

        return True
