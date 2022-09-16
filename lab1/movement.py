#!/usr/bin/env python3

from time import sleep
from math import sin, cos, radians

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import GyroSensor

class MoveHandler:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

        self.gs = GyroSensor()
        self.gs.mode = 'GYRO-ANG'
        self.gs.reset()
        
        self.dir = -1       # Flip motor direction to match the orientation of our motors

    def move(self, left_speed, right_speed, seconds):
        # Reset motor positions and gyro sensor angle so relative motion can be calculated
        self.tank_drive.left_motor.position = 0
        self.tank_drive.right_motor.position = 0
        self.gs.reset()

        # Change direction to match our motor orientation
        left_speed *= self.dir
        right_speed *= self.dir
        
        self.tank_drive.on_for_seconds(left_speed, right_speed, seconds)

        self.print_position(seconds)
        #self.print_gyro()

    def print_gyro(self):
        print(str(self.gs.angle))

    def wheel_speed(self, wheel, seconds):
        # Return wheel speed in cm/s
        # Wheel speed:
        # degrees / (degrees per rotation) * (wheel circumference) / seconds
        # wheel diameter: 5.6cm, circumference: 17.6

        # Note: Sign of speed is changed to match the orientation of our motors
        return self.dir * wheel.position / 360 * 17.6 / seconds

    
    def print_position(self, seconds):
        # Use kinematics to find position
        
        # Given wheel speeds, compute x, y, theta
        v1 = self.wheel_speed(self.tank_drive.left_motor, seconds)
        v2 = self.wheel_speed(self.tank_drive.right_motor, seconds)

        # Total velocity is sum of both wheels divided by 2
        v = (v1 + v2) / 2

        # Multiply v by cos theta for vx and sin theta for vy
        theta = self.gs.angle
        vx = v * cos(radians(theta))
        vy = v * sin(radians(theta))

        # Multiply by time to find position (cm)
        x = vx * seconds
        y = vy * seconds

        print("theta %d degrees" % theta)
        print("x: %d cm" % x)
        print("y: %d cm" % y)
        print("-")
            

def main():
    # Left motor speed, right motor speed, seconds
    commands = [
        [ 60, 60, 5 ],
        [ 60, 30, 2 ]
    ]
    
    moveHandler = MoveHandler()

    for command in commands:
        moveHandler.move(command[0], command[1], command[2])
        sleep(1)
    
    # Sleep so the user can read the screen output
    sleep(20)

if __name__ == "__main__":
    main()