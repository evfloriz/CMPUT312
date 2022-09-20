#!/usr/bin/env python3

from time import sleep
from math import sin, cos, radians, pi

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds

class MoveHandler:
    
    # Axel (cm)
    axelLength = 10.5

    # Wheel (cm)
    wheelDiameter = 5.6
    wheelCircumference = pi*wheelDiameter

    # Motor (rotations per second)
    motorRPS = 165/60
    motorDirection = -1

    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

        # Initiate gyro sensor
        self.gs = GyroSensor()
        self.gs.mode = 'GYRO-ANG'
        self.gs.reset()
        
    def move(self, left_speed, right_speed, seconds):
        # Reset motor positions and gyro sensor angle so relative motion can be calculated
        self.tank_drive.left_motor.position = 0
        self.tank_drive.right_motor.position = 0
        self.gs.reset()

        # Change direction to match our motor orientation
        left_speed *= MoveHandler.motorDirection
        right_speed *= MoveHandler.motorDirection
        
        self.tank_drive.on_for_seconds(left_speed, right_speed, seconds)

        odom = self.print_position(seconds)
        #self.print_gyro()
        
        return odom

    def drive(self, distance, direction, velocity):
        
        # Compute variables for kinematics
        time = distance/velocity
        angularVelocity = velocity/(MoveHandler.wheelDiameter/2)
        percent = angularVelocity*100/(2*pi)/MoveHandler.motorRPS
        print(time)
        print(angularVelocity)
        
        # Move based on direction input
        if direction is "forwards":
        
            self.move(SpeedPercent(percent), SpeedPercent(percent), time)
            
        elif direction is "backwards":
            
            self.move(-SpeedPercent(percent), -SpeedPercent(percent), time)

    def spin(self, degrees, direction, velocity):
        
        # Compute variables for kinematics
        radians = degrees*(pi/180)
        distance = radians*(MoveHandler.axelLength/2)
        time = distance/velocity
        
        # Compute wheel velocity based on direction input
        if direction is "right":
            
            leftVelocity = -velocity
            rightVelocity = velocity
            
        elif direction is "left":

            leftVelocity = velocity
            rightVelocity = -velocity
            
        # Compute angular velocity for each wheel
        leftAngularVelocity = leftVelocity/(2*pi)/(MoveHandler.wheelDiameter/2)
        rightAngularVelocity = rightVelocity/(2*pi)/(MoveHandler.wheelDiameter/2)
        
        # Compute motor power percent for each wheel and move accordingly
        leftPercent = leftAngularVelocity*100/MoveHandler.motorRPS
        rightPercent = rightAngularVelocity*100/MoveHandler.motorRPS
        self.move(SpeedPercent(leftPercent), SpeedPercent(rightPercent), time)

    def turn(self, degrees, turnRadius, direction, velocity):
        
        # Compute variables for kinematics
        radians = degrees*(pi/180)
        distance = radians*turnRadius
        time = distance/velocity
        angularVelocity = radians/time
        angularVelocity = angularVelocity/(2*pi)
        
        # Compute wheel velocity based on direcction input
        if direction is "right":
            
            leftVelocity = (turnRadius+(MoveHandler.axelLength/2))*angularVelocity
            rightVelocity = (turnRadius-(MoveHandler.axelLength/2))*angularVelocity
            
        elif direction is "left":

            leftVelocity = (turnRadius-(MoveHandler.axelLength/2))*angularVelocity
            rightVelocity = (turnRadius+(MoveHandler.axelLength/2))*angularVelocity
            
        # Compute angular velocity for each wheel
        leftAngularVelocity = leftVelocity/(MoveHandler.wheelDiameter/2)
        rightAngularVelocity = rightVelocity/(MoveHandler.wheelDiameter/2)
        
        # Compute motor power percent for each wheel and move accordingly
        leftPercent = leftAngularVelocity*100/MoveHandler.motorRPS
        rightPercent = rightAngularVelocity*100/MoveHandler.motorRPS
        self.move(SpeedPercent(leftPercent), SpeedPercent(rightPercent), time)
    
    def print_gyro(self):
        print(str(self.gs.angle))

    def wheel_speed(self, wheel, seconds):
        # Return wheel speed in cm/s
        # Wheel speed:
        # degrees / (degrees per rotation) * (wheel circumference) / seconds
        # wheel diameter: 5.6cm, circumference: 17.6

        # Note: Sign of speed is changed to match the orientation of our motors
        return MoveHandler.motorDirection * wheel.position / 360 * 17.6 / seconds
    
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
        
        return {"x": x, "y": y, "theta": theta}
