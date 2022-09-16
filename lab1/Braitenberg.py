#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds

class Braitenberg:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        #self.move = MoveSteering(OUTPUT_A, OUTPUT_B)        # need to flip motors to drive forward
        
        self.cs1 = ColorSensor(INPUT_3)       # right sensor
        self.cs2 = ColorSensor(INPUT_4)       # left sensor
        
        self.cs1.mode = 'COL-AMBIENT'
        self.cs2.mode = 'COL-AMBIENT'

    def follow_light(self):
        while (True):
            #diff = self.cs1.value() - self.cs2.value()

            # follow the difference in sensors for half a second
            #self.move.on_for_seconds(diff, SpeedPercent(60), 0.5)
            #print(diff)
            #self.move.on(diff, SpeedPercent(30))

            left_speed = self.cs1.value() * 2
            right_speed = self.cs2.value() * 2

            self.tank_drive.on(left_speed, right_speed)
            sleep(0.5)

    def aggression(self):
        while(True):
            # Move towards light
            left_speed = self.cs1.value() * 2
            right_speed = self.cs2.value() * 2

            self.tank_drive.on(left_speed, right_speed)
            sleep(0.5)

    def cowardice(self):
        while(True):
            # Charge toward light if straight ahead, otherwise move away
            left_speed = self.cs2.value() * 2
            right_speed = self.cs1.value() * 2

            self.tank_drive.on(left_speed, right_speed)
            sleep(0.5)

    def love(self):
        while(True):
            # Non linear, move slow if dark or bright, move fast if medium
            left_speed = (self.cs1.value() / 5 - 20) ** 2
            right_speed = (self.cs2.value() / 5 - 20) ** 2

            self.tank_drive.on(left_speed, right_speed)
            sleep(0.5)


def main():
    braitenberg = Braitenberg()
    #braitenberg.follow_light()
    braitenberg.aggression()

if __name__ == "__main__":
    main()