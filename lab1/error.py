#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

class MoveHandler:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        
        self.dir = -1
        self.speed = 50
        self.rotations = 5

    def run(self):
        left_speed = self.speed * self.dir
        right_speed = self.speed * self.dir
        
        self.tank_drive.on_for_rotations(left_speed, right_speed, self.rotations)


def main():
    moveHandler = MoveHandler()
    moveHandler.run()

if __name__ == "__main__":
    main()