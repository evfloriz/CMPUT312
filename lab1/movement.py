#!/usr/bin/env python3

'''
"""
Group Members: Evan Florizone, Yiyan Zhang

Date: Sept 21, 2022
 
Brick Number: g10

Lab Number: 1

Problem Number: 2, 3, 4
 
Brief Program/Problem Description: 

	Implement a movement class to handle common movement functions.

Brief Solution Summary:

	move - actually move motors using motor speeds
    drive - kinematically determine motor speed given a distance, direction and velocity and move motors accordingly
    spin - kinematically determine motor speed given a degree, direction and velocity and move motors accordingly
    turn - kinematically determine motor speed given a degree, turn radius, direction and velocity and move motors accordingly
    calculate_position - calculate position kinematically given motor speeds and time
    write_state_to_file - write motor and sensor data to file

    Other helper functions are implemented to facilitate this core functionality

Used Resources/Collaborators:
	ev3dev API,
    ev3dev tutorial https://sites.google.com/site/ev3python/learn_ev3_python

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""
'''

from time import sleep
from math import sin, cos, radians, pi, degrees

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

    def __init__(self, file):        
        self.file = file

        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

        # Initiate gyro sensor
        self.gs = GyroSensor()
        self.gs.mode = 'GYRO-ANG'
        self.gs.reset()
        #self.gs.calibrate()            # may need to calibrate if gyro angle changes on its own
        
        # Keep track of accumulated odometry readings
        self.pos = {"x": 0, "y": 0, "theta": 0}
        self.power = [0, 0]

        self.start_angle = 0
        
    def move(self, left_speed, right_speed, seconds):
        # Reset motor positions and gyro sensor angle so relative motion can be calculated
        self.tank_drive.left_motor.position = 0
        self.tank_drive.right_motor.position = 0
        self.gs.reset()

        # Change direction to match our motor orientation
        left_speed *= MoveHandler.motorDirection
        right_speed *= MoveHandler.motorDirection
        
        self.tank_drive.on_for_seconds(left_speed, right_speed, seconds)

        self.power = [left_speed, right_speed]
        self.calculate_position(seconds)
        
        self.write_state_to_file()

    def drive(self, distance, direction, velocity):
        
        # Compute variables for kinematics
        time = distance/velocity
        angularVelocity = velocity/(MoveHandler.wheelDiameter/2)
        percent = angularVelocity*100/(2*pi)/MoveHandler.motorRPS
        
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
        if direction is "left":
            
            leftVelocity = -velocity
            rightVelocity = velocity
            
        elif direction is "right":

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
        # wheel diameter: 5.6cm, circumference: 5.6 * pi

        # Note: Sign of speed is changed to match the orientation of our motors
        return MoveHandler.motorDirection * wheel.position / 360 * (5.6 * pi) / seconds
    
    def calculate_position(self, seconds):
        # Use kinematics to find position
        
        # Given wheel speeds, compute x, y, theta
        vl = self.wheel_speed(self.tank_drive.left_motor, seconds)
        vr = self.wheel_speed(self.tank_drive.right_motor, seconds)

        #self.file.write("vl: " + str(vl) + " cm/s\n" +
        #                "vr: " + str(vr) + " cm/s\n")

        # Total velocity is sum of both wheels divided by 2
        v = (vr + vl) / 2

        # Compute angular velocity and the final angle (radians)
        a = (vr - vl) / MoveHandler.axelLength
        theta = a * seconds

        # Multiply v by cos theta / 2 for vx and sin theta for vy
        # Theta is divided by 2 to find the average angle from the final angle (assuming a circular turn)
        avg_theta = theta / 2
        vx = v * cos(avg_theta)
        vy = v * sin(avg_theta)

        #self.file.write("vx: " + str(vx) + " cm/s\n" +
        #                "vy: " + str(vy) + " cm/s\n")

        # Multiply by time to find position (cm) in robot reference frame [xr, yr]
        xr = vx * seconds
        yr = vy * seconds
        
        # Convert coordinates from robot reference frame to world reference frame [xw, yw] using rotation matrix
        # From Robotics, Modeling, and Control, section 2.2.1, page 41
        xw = xr * cos(self.start_angle) - yr * sin(self.start_angle)
        yw = xr * sin(self.start_angle) + yr * cos(self.start_angle)

        #self.file.write("xr: " + str(xr) + " cm\n" +
        #                "yr: " + str(yr) + " cm\n" +
        #                "xw: " + str(xw) + " cm\n" +
        #                "yw: " + str(yw) + " cm\n")

        # Update accumulated position
        self.pos["x"] += xw
        self.pos["y"] += yw
        self.pos["theta"] += degrees(theta)

        # Update current heading for next calculation (in radians)
        self.start_angle += theta

    def write_pos(self):
        self.file.write("x: "       + str(self.pos["x"])        + " cm\n" +
                        "y: "       + str(self.pos["y"])        + " cm\n" +
                        "theta: "   + str(self.pos["theta"])    + " degrees\n")

    def write_gyro(self):
        # Gyro angle is negative to match our motor orientation
        self.file.write("gyro: " + str(-self.gs.angle) + " degrees\n")
    
    def write_power(self):
        self.file.write("left power: " + str(self.power[0]) + " percent\n" +
                "right power: " + str(self.power[1]) + " percent\n")

    def write_state_to_file(self):
        self.write_pos()
        self.write_gyro()
        self.write_power()
        self.file.write("---------------------------------------------\n")
