#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

import time
from tracemalloc import start
from server import Server
from color_tracking import Tracker
from queue import Queue
from math import sin, asin, acos, atan2, degrees, sqrt
import numpy as np

connect = False

class Controller:
    
    def __init__(self):
        #self.host = "142.244.172.63"
        self.host = "172.17.0.1"

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
        return [self.tracker.point[0], self.tracker.goal[0]]
    
    
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
        point2, goal2 = self.track()
        
        if (connect):
            self.sendAngles(0, theta2_wiggle)
            time.sleep(1)
        
        point3, goal3 = self.track()
        
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
        error_size = 50
     
        # Wiggle and initialize jacobian
        jacobian = self.initialize()
        
        # Get initial robot u and v and error
        point, goal = self.track()
        points = np.array(point[0])
        counter = 0

        error = np.array([[goal[0] - point[0]], [goal[1] - point[1]]])
        error_norm = np.linalg.norm(error)

        print(error)
        print(error_norm)

        return
        
        # Broyden update
        while (error_norm > error_size):
            
            
            
            if i == 3:
                self.exit()
                
            print(jacobian)
            print(error)
            print(np.sqrt(error[0]**2+error[1]**2))
            
            # Get theta and move robot
            #theta = np.matmul(lambd*jacobian, error)
            theta = np.matmul(lambd*np.linalg.pinv(jacobian), error)
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
        if (connect):
            self.server.sendTermination()
            print("Exiting server")
            time.sleep(1)

    def print_data(self):
        data = self.track()
        print("u: " + str(data[0]))
        print("v: " + str(data[1]))
        #print("u - v: [" + str(data[0][0] - data[1][0]) + " " + str(data[0][1] - data[1][1]) + "]")
        
        #print(str(data[0][0][0]))
        #print("---------------")
        #print(data)


def main():
    controller = Controller()
    
    #controller.initialize()
    
    while (True):
        #controller.print_data()
        controller.uvs()
        time.sleep(1)
    
    #controller.uvs(1, 0.2, 50)
    
    controller.exit()

main()

        
