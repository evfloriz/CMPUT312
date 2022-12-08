#!/usr/bin/env python3

import hello
import os
import sys
from time import sleep
import math
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor

# state constants
ON = True
OFF = False
class GyroMovement:

    def __init__(self):
        self.fullStepSize = 3 #cm
        self.hip_width = 96 #mm
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)

        self.horizontalGyro = GyroSensor(INPUT_2)
        self.verticalGyro = GyroSensor(INPUT_1)

    def shuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        
        
        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        self.verticalGyro.reset()
        self.verticalGyro.calibrate
        
        horizontalStart = self.horizontalGyro.angle

        while(self.horizontalGyro.angle - horizontalStart > -24):  
            self.leftHip.on(5, brake=False)
            self.rightHip.on(-4, brake=False)

            hello.debug_print(self.horizontalGyro.angle)

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        sleep(1)
        return True

    def shuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        self.verticalGyro.reset()
        self.verticalGyro.calibrate
        
        horizontalStart = self.horizontalGyro.angle

        while(self.horizontalGyro.angle - horizontalStart < 24):  
            self.rightHip.on(5, brake=False)
            self.leftHip.on(-5, brake=False)
            
            hello.debug_print(self.horizontalGyro.angle)

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        sleep(1)
        return True


    def liftRight(self):

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        #Lift using on motor test 
        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        self.verticalGyro.reset()
        self.verticalGyro.calibrate

        horizontalStart = self.horizontalGyro.angle
        verticalStart = self.verticalGyro.angle
        
        hello.debug_print("Lift Right")
        while(self.verticalGyro.angle > -18):  
            self.rightAnkle.on(-18, brake= False)
            self.leftAnkle.on(10, brake=False)
            
            hello.debug_print(self.verticalGyro.angle)

        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)


        sleep(2)
        return True

    def lowerRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(15), -170, brake=False, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(25), 280, brake=False, block=True)
        sleep(1)
        return True


    #Add Gyro to these lifting classes first

    def liftLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        #Lift using on motor test 
        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        self.verticalGyro.reset()
        self.verticalGyro.calibrate

        horizontalStart = self.horizontalGyro.angle
        verticalStart = self.verticalGyro.angle
        
        hello.debug_print("Lift Left")
        while(self.verticalGyro.angle - verticalStart < 18):  
            self.leftAnkle.on(-18, brake=False)
            self.rightAnkle.on(10, brake= False)
            hello.debug_print(self.verticalGyro.angle)

        self.leftAnkle.off(brake=False)
        self.rightAnkle.off(brake=True)

        sleep(2)
        return True

    def lowerLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(15), -170, brake=False, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(25), 280, brake=False, block=True)
        sleep(1)
        return True

    def rotateLeft(self, angle):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftHip.on_for_degrees(SpeedPercent(25), angle*5, brake=True, block=True)
        sleep(1)
        return True

    def rotateRight(self, angle):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(25), angle*5, brake=True, block=True)
        sleep(1)
        return True

    def halfStepRight(self):
        #Half a shuffle
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        
        
        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        
        horizontalStart = self.horizontalGyro.angle

        while(self.horizontalGyro.angle - horizontalStart > -4):  
            self.rightHip.on(-6, brake=False)
            self.leftHip.on(7, brake=False)
            
            hello.debug_print(self.horizontalGyro.angle)

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        sleep(1)
        return True

    def halfStepLeft(self):
        #Implement with gyroscopes
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        
        #Calibrate the gryoscope. 
        self.horizontalGyro.reset()
        self.horizontalGyro.calibrate()
        
        #Get the starting angle of the gyroscopes
        horizontalStart = self.horizontalGyro.angle

        #While we havent reached our desired angle we continue to rotate
        while(self.horizontalGyro.angle - horizontalStart < 4):  
            self.leftHip.on(-6, brake=False)
            self.rightHip.on(7, brake=False)

        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        sleep(1)
        return True


    def firstStepRight(self):
        #The initial first step taking only half a step to maintain forward orientation
        self.liftRight()
        self.halfStepRight()
        self.lowerRight()

    def lastStepLeft(self):
        #Use this last step with left foot to even out feet after walking
        self.liftLeft()
        self.halfStepLeft()
        self.lowerLeft()

    def stepRight(self):
        #Implement the lift and shuffle methods to take a full right foot step
        self.liftRight()
        self.shuffleRight()
        self.lowerRight()
        return True

    def stepLeft(self):
        #Implement the lift and shuffle methods to take a full left foot step 
        self.liftLeft()
        self.shuffleLeft()
        self.lowerLeft()
        return True

    def walk(self, distance):
        #Take in a desired distance and walk that far. 
        self.firstStepRight()
        traveledDistance = 2.3 #cm
        #These distances are measured in testing. 
        while(distance - traveledDistance > 0):
            self.stepLeft()
            self.stepRight()
            traveledDistance += 7.5 #cm
        
        #Even out the feet
        self.lastStepLeft()
