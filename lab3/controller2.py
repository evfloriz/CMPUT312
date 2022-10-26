#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

import time
from tracemalloc import start
from server import Server
from color_tracking import Tracker
from queue import Queue
from math import sin, asin, acos, atan2, degrees, sqrt
import numpy as np

class Controller:
    
    def __init__(self):
        self.host = "142.244.172.63"
        #host = "localhost"
        self.port = 9999
        self.tracker = Tracker('b', 'r')
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
        print("Tracker Setup")
        print("Moving on")
        return self.tracker.point[0][0], self.tracker.point[0][1], self.tracker.goal[0][0], self.tracker.goal[0][1]
    
    
    def initialize(self, theta1_wiggle, theta2_wiggle):
        
        # Get robot u and v
        point_u, point_v, tracker_u, tracker_v = self.track()
        
        # Wiggle robot
        self.sendAngles(theta1_wiggle, 0)
        time.sleep(1)
        # Get robot u and v
        point_u1, point_v1, tracker_u, tracker_v = self.track()
        
        self.sendAngles(0, theta2_wiggle)
        time.sleep(1)
        
        point_u2, point_v2, tracker_u, tracker_v = self.track()
        
        return np.array([[(point_u1-point_u)/theta1_wiggle, (point_u2-point_u1)/theta2_wiggle],
                  [(point_v1-point_v)/theta1_wiggle, (point_v2-point_v1)/theta2_wiggle]])
        
        # Return initial Jacobian
        #return np.array([[abs(point_u-point_u1)/theta1_wiggle, abs(point_u-point_u1)/theta2_wiggle], [abs(point_v-point_v1)/theta1_wiggle, abs(point_v-point_v1)/theta2_wiggle]])
    
    
    def uvs(self, alpha, lambd, error_size):
        
        # Initialize u and v points
        u_points = np.zeros(1)
        v_points = np.zeros(1)
        counter = 0
        
        # Wiggle and initialize jacobian
        jacobian = self.initialize(20,20)
        
        # Get initial robot u and v and error
        point_u, point_v, tracker_u, tracker_v = self.track()
        u_points[0] = point_u
        v_points[0] = point_v
        error = np.array([[(tracker_u - point_u)], [-(tracker_v - point_v)]])
        
        # Broyden update
        i = 0
        while (np.sqrt(error[0]**2+error[1]**2) > error_size):
            
            if i == 3:
                self.exit()
                
            print(jacobian)
            print(error)
            print(np.sqrt(error[0]**2+error[1]**2))
            
            # Get theta and move robot
            #theta = np.matmul(lambd*jacobian, error)
            theta = lambd * np.matmul(np.linalg.pinv(jacobian), error)
            print(theta)
            self.sendAngles(theta[0][0], theta[1][0])
            time.sleep(1)
            i += 1
            if (i % 3 < 0):
                continue
            
            # Read points
            point_u, point_v, tracker_u, tracker_v = self.track()
            u_points = np.append(u_points, point_u)
            v_points = np.append(v_points, point_v)
            counter+=1    
            
            # Update jacobian
            error = np.array([[(tracker_u - point_u)], [-(tracker_v - point_v)]])
            q_delta = np.matmul(np.linalg.pinv(jacobian), error)
            y_delta = np.array([[u_points[counter] - u_points[counter-1]], [v_points[counter] - v_points[counter-1]]])
            j1 = np.matmul(jacobian, q_delta)
            j2 = np.matmul(q_delta.T, q_delta)
            j3 = np.divide((y_delta - j1), j2)
            jacobian = jacobian + alpha*np.matmul(j3, q_delta.T)
        

    def exit(self):
        self.server.sendTermination()
        print("Exiting server")
        time.sleep(1)


def main():
    controller = Controller()
    
    controller.uvs(1, 0.2, 50)
    
    controller.exit()

main()

        
