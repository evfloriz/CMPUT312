#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import GyroSensor
from time import sleep

class Robot:
    def __init__(self):
        self.file = open("gyrowalk.out", "w")
        
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)

        self.hipGyro = GyroSensor(INPUT_1)    # hip motion gyro
        self.ankleGyro = GyroSensor(INPUT_2)    # ankle motion gyro
        
        self.ankleGyro.calibrate()
        self.hipGyro.calibrate()
        
        self.file.write("start\n")
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")

    def liftRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), 110, brake=True, block=True)
        self.file.write("leftRight gyro\n")
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)

    def lowerRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), -110, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)
        self.file.write("lowerRight gyro\n")
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)

    def liftLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.leftAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), 110, brake=True, block=True)
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)

    def lowerLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), -110, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)

    def shuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(10), -70, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(10), 70, brake=True, block=True)
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)

    def shuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.on_for_degrees(SpeedPercent(10), 70, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(10), -70, brake=True, block=True)
        self.file.write("ankle gyro: " + str(self.ankleGyro.angle) + "\n")
        self.file.write("hip gyro: " + str(self.hipGyro.angle) + "\n")
        sleep(1)


    def firstStepRight(self):
        self.liftRight()
        self.shuffleRight()
        self.lowerRight()

    def stepRight(self):
        self.liftRight()
        self.shuffleRight()
        self.shuffleRight()
        self.lowerRight()

    def stepLeft(self):
        self.liftLeft()
        self.shuffleLeft()
        self.shuffleLeft()
        self.lowerLeft()


def main():
    robot = Robot()

    robot.firstStepRight()
    robot.stepLeft()
    robot.stepRight()

    # final pos
    robot.shuffleLeft()
    

main()

