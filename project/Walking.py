#!/usr/bin/env python3
import hello
import os
import sys
from time import sleep
import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor

# state constants
ON = True
OFF = False
class Movement:

    def __init__(self, distance, speed):
        self.distance = distance 
        self.speed = speed
        self.hip_width = 96 #mm
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)
        

    def walk(self, fullStepSize):
        # Calculate First step size and perform
        halfStep = fullStepSize/2
        # self.firstAndLastStep(halfStep)
        self.firstStepRight()
        #Add step length to total distance
        totalDistance = halfStep

        #Perform walking until we reach the desired distance
        while (self.distance - totalDistance) > 0:
            self.step(fullStepSize)
            totalDistance += fullStepSize*2
        
        # even out feet at end
        self.shuffleLeft()
        
        final_distance = str(self.distance)
        #Print total distance traveled
        hello.debug_print("walked aproximately " + final_distance + "mm")
        
        return True

    def firstStepRight(self):
        #first step
        self.liftRight()
        self.shuffleRight()
        self.lowerRight()
        return True


    def step(self, FullStepSize):
        #Left foot full step
        hipRotation = math.degrees(math.asin(FullStepSize/self.hip_width))

        self.stepLeft()
        self.stepRight()

        return True


    def liftRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), 110, brake=True, block=True)
        sleep(1)
        return True

    def lowerRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), -110, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)
        sleep(1)
        return True

    def liftLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), 110, brake=True, block=True)
        sleep(1)
        return True

    def lowerLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), -110, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)
        sleep(1)
        return True

    def shuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(10), -70, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(10), 70, brake=True, block=True)
        sleep(1)
        return True

    def shuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(10), 70, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(10), -70, brake=True, block=True)
        sleep(1)
        return True


    def stepRight(self):
        self.liftRight()
        self.shuffleRight()
        self.shuffleRight()
        self.lowerRight()
        return True

    def stepLeft(self):
        self.liftLeft()
        self.shuffleLeft()
        self.shuffleLeft()
        self.lowerLeft()
        return True