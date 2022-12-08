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

    def __init__(self, speed):
        self.speed = speed
        self.hip_width = 96 #mm
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)
        

    def walk(self, distance, fullStepSize):
        # Calculate First step size and perform
        halfStep = fullStepSize/2
        # self.firstAndLastStep(halfStep)
        self.firstStepRight()
        #Add step length to total distance
        totalDistance = halfStep

        #Perform walking until we reach the desired distance
        while (distance - totalDistance) > 0:
            self.step(fullStepSize)
            totalDistance += fullStepSize*2
        
        # even out feet at end
        self.shuffleLeft()
        
        final_distance = str(distance)
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
        self.rightHip.on_for_degrees(SpeedPercent(15), -20*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), 20*5, brake=True, block=True)
        sleep(1)
        return True

    def shuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(15), 20*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), -20*5, brake=True, block=True)
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
    
    def right(self, angle):
        compensation = 20
        self.liftLeft()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.on_for_degrees(SpeedPercent(15), compensation*5, brake=True, block=False)
        self.rightHip.on_for_degrees(SpeedPercent(15), angle*5, brake=True, block=False)
        sleep(3)
        self.lowerLeft()
        self.liftRight()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.on_for_degrees(SpeedPercent(15), -compensation*5, brake=True, block=False)
        self.rightHip.on_for_degrees(SpeedPercent(15), -angle*5, brake=True, block=False)
        sleep(3)
        self.lowerRight()
        
    def left(self, angle):
        compensation = 20
        self.liftRight()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(15), compensation*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), angle*5, brake=True, block=False)
        sleep(3)
        self.lowerRight()
        self.liftLeft()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(15), -compensation*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), -angle*5, brake=True, block=False)
        sleep(3)
        self.lowerLeft()

    def turnRight(self, angle):
        if angle <= 45:
            self.right(angle)
        else:
            repeat = math.floor(angle/45)
            remain = angle % 45
            for i in range(repeat):
                self.right(45)
            if math.floor(remain) != 0:
                self.right(remain)
                
    def turnLeft(self, angle):
        if angle <= 45:
            self.left(angle)
        else:
            repeat = math.floor(angle/45)
            remain = angle % 45
            for i in range(repeat):
                self.left(45)
            if math.floor(remain) != 0:
                self.left(remain)
        
    def turnRight2(self, angle):
        self.liftRight()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.on_for_degrees(SpeedPercent(10), -angle*5/2, brake=True, block=False)
        sleep(5)
        self.rightHip.on_for_degrees(SpeedPercent(10), -angle*5/2, brake=True, block=False)
        sleep(5)
        self.lowerRight()
        self.liftLeft()
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.on_for_degrees(SpeedPercent(10), angle*5/2, brake=True, block=False)
        sleep(5)
        self.rightHip.on_for_degrees(SpeedPercent(10), angle*5/2, brake=True, block=False)
        sleep(5)
        self.lowerLeft()
        

def main():
    
    robot = Movement(50)
    robot.walk(500, 50)
    robot.turnRight(90)
    robot.walk(500, 50)
    
    
main()