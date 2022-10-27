#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

'''
Group Members: Evan Florizone, Yiyan Zhang

Date: Oct 26, 2022
 
Brick Number: g10

Lab Number: 3

Problem Number: 2
 
Brief Program/Problem Description:
    Handle server-side code for the robot. The goal is to use visual servoing
    to move toward a goal point.

Brief Solution Summary:
    sendAngles - send angles to the client and wait for a response.
    track - receive the positions of point and goal from the color tracker. In
    order to smooth some of the jittery data, 10 points are read at 0.05 second
    intervals and the average is returned.
    initialize - create the initial Jacobian by wiggling first the base motor,
    then the joint motor and recording the change in pixel values tracked by
    the color tracker.
    uvs - perform uncalibrated visual servoing. First initialize is called and the
    first point is read in including the error. Then find q_delta from initial error
    and Jacobian, then move the robot those angles and record the y_delta and error
    after the motion. Then update the Jacobian using the previous Jacobian, q_delta,
    y_delta, and error using Broyden's method. Repeat until the error is within the
    specified amount.

Used Resources/Collaborators:
    uvs3.jpg - lab notes
    visual servoing lecture slides
    color_tracking.py
    server.py
	
I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
'''

import time
from tracemalloc import start
from server import Server
from color_tracking import Tracker
from queue import Queue
from math import sin, asin, acos, atan2, degrees, sqrt
import numpy as np

connect = True

class Controller:
    
    def __init__(self):
        host = "142.244.173.149"
        #host = "172.17.0.1"

        #host = "localhost"
        self.port = 9999
        self.tracker = Tracker('b', 'r')
        
        if (connect):
            self.server = Server(self.host, self.port)
        self.queue = Queue()

        # Length of link 1 and 2 in cm
        self.l1 = 16.0
        self.l2 = 8.5
        

    def sendAngles(self, motor1_degrees, motor2_degrees):
        print(motor1_degrees)
        print(motor2_degrees)
        self.server.sendAngles(motor1_degrees, motor2_degrees, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def track(self):
        avg_point = [0, 0]
        avg_goal = [0, 0]

        num = 10

        for i in range(num):
            avg_point[0] += self.tracker.point[0][0]
            avg_point[1] += self.tracker.point[0][1]

            avg_goal[0] += self.tracker.goal[0][0]
            avg_goal[1] += self.tracker.goal[0][1]

            time.sleep(0.05)

        avg_point[0] /= num
        avg_point[1] /= num
        avg_goal[0] /= num
        avg_goal[1] /= num

        return [avg_point, avg_goal]
    
    
    def initialize(self):
        theta1_wiggle = 20
        theta2_wiggle = 20
        
        # keep looking until a valid goal has been found
        goal = [0, 0, 0]
        point1 = [0, 0, 0]
        while (goal[0] == 0 or goal[1] == 0):
            # Get robot u and v
            point1, goal = self.track()
            #print(goal)
        
        # Wiggle robot
        if (connect):
            self.sendAngles(theta1_wiggle, 0)
            time.sleep(1)

        # Get robot u and v
        point2, goal = self.track()
        
        if (connect):
            self.sendAngles(0, theta2_wiggle)
            time.sleep(1)
        
        point3, goal = self.track()
        
        # Return initial Jacobian
        dudt1 = (point2[0] - point1[0])/theta1_wiggle
        dudt2 = (point3[0] - point2[0])/theta2_wiggle
        dvdt1 = (point2[1] - point1[1])/theta1_wiggle
        dvdt2 = (point3[1] - point2[1])/theta2_wiggle

        return np.array([[dudt1, dudt2],
                        [dvdt1, dvdt2]])
            
    
    def uvs(self):
        # parameters
        a = 1
        l = 0.1
        error_size = 100
     
        # Wiggle and initialize jacobian
        jacobian = self.initialize()
        
        # Get initial robot u and v and error
        point, goal = self.track()
        oldPoint = point
        counter = 0

        error = np.array(   [[goal[0] - point[0]],
                            [goal[1] - point[1]]])
        error_norm = np.linalg.norm(error)
        
        # Broyden update
        while (error_norm > error_size):
            print("Error:")
            print(error)
            print("Error norm: " + str(error_norm))

            print("Jacobian:")
            print(jacobian)

            q_delta = l * np.matmul(np.linalg.pinv(jacobian), error)
            self.sendAngles(q_delta[0][0], q_delta[1][0])
            time.sleep(1)

            # Read points
            point, goal = self.track()
            
            # Update jacobian
            error = np.array(   [[goal[0] - point[0]],
                                [goal[1] - point[1]]])

            y_delta = np.array( [[point[0] - oldPoint[0]],
                                [point[1] - oldPoint[1]]])

            j1 = np.matmul(jacobian, q_delta)
            j2 = np.matmul(q_delta.T, q_delta)
            j3 = np.divide((y_delta - j1), j2)
            jacobian = jacobian + a * np.matmul(j3, q_delta.T)

            # Update error norm
            error_norm = np.linalg.norm(error)

            # Update old point
            oldPoint = point
        

    def exit(self):
        if (connect):
            self.server.sendTermination()
            print("Exiting server")
            time.sleep(1)

    def print_data(self):
        data = self.track()
        print("u: " + str(data[0]))
        print("v: " + str(data[1]))
        #print("u - v: [" + str(data[0][0] - data[1][0]) + " " + str(data[0][1] - data[1][1]) + "]")
        print("---------------")


def main():
    controller = Controller()
    
    controller.uvs()
    time.sleep(1)
    
    controller.exit()

main()

        
