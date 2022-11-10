#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
from time import sleep

class Robot:
    def __init__(self):
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)

    def liftRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(5), 25, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(5), -25, brake=True, block=True)
        sleep(1)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), -10, brake=True, block=False)
        sleep(2)

    def lowerRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), 25, brake=True, block=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), -30, brake=True, block=True)
        sleep(2)

    def shuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(10), -15, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(10), 15, brake=True, block=True)
        #sleep(2)


def main():
    robot = Robot()
    robot.liftRight()
    robot.shuffleRight()
    robot.lowerRight()

main()