#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

class MoveHandler:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

        self.gs = GyroSensor()
        self.gs.mode = 'GYRO-ANG'
        self.gs.reset()
        
        self.dir = -1
        self.speed = 60
        self.rotations = 10
        #self.seconds = 5

        self.rate = 0.5

    def run(self):
        self.forward_kinematics()
        self.print_gyro()
        
        left_speed = self.speed * self.dir
        right_speed = self.speed * self.dir
        
        self.tank_drive.on_for_rotations(left_speed, right_speed, self.rotations)
        #self.tank_drive.on_for_seconds(left_speed, right_speed, self.seconds)

        self.forward_kinematics()
        self.print_gyro()

    def print_gyro(self):
        print(str(self.gs.angle))
        #sleep(self.rate)

    def forward_kinematics(self):
        # given wheel speeds, compute x, y, theta
        # wheel speeds:
        # rotations per second converted into distance per second

        
        print(str(self.tank_drive.left_motor.position))
        print(str(self.tank_drive.right_motor.position))



def main():
    moveHandler = MoveHandler()
    moveHandler.run()
    #moveHandler.print_gyro()
    #moveHandler.forward_kinematics()
    sleep(20)

if __name__ == "__main__":
    main()