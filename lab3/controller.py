#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

import time
from tracemalloc import start
from server import Server
from queue import Queue
from math import sin, asin, acos, atan2, degrees, sqrt

class Controller:
    def __init__(self):
        self.host = "172.17.0.1"
        #host = "localhost"
        self.port = 9999
        self.server = Server(self.host, self.port)
        self.queue = Queue()

        # Length of link 1 and 2 in cm
        self.l1 = 16.0
        self.l2 = 8.5
        

    def sendAngles(self, motor1_degrees, motor2_degrees):
        self.server.sendAngles(motor1_degrees, motor2_degrees, self.queue)            
        response = self.queue.get()
        print("Received: " + response)


    def straightLine(self, pos1, pos2):
        trajectory = []
        
        numSteps = 10

        step = [pos2[0] - pos1[0], pos2[1] - pos1[1]]
        step = [step[0] / numSteps, step[1] / numSteps]

        print(step)
        
        # Go to the first pos and initialize values to update iteratively
        angles = self.buildTrajectory(trajectory, [0, 0], pos1)
        stepPos = pos1

        i = 0
        while (i < numSteps):
            stepPos = [stepPos[0] + step[0], stepPos[1] + step[1]]
            print(stepPos)
            angles = self.buildTrajectory(trajectory, angles, stepPos)
            i += 1

        self.executeTrajectory(trajectory)

    def buildTrajectory(self, trajectory, startAngles, pos):
        x = pos[0]
        y = pos[1]

        # Calculate motor angles geometrically
        theta2 = acos((x**2 + (y**2) - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2))
        theta1 = asin((self.l2 * sin(theta2)) / sqrt(x**2 + y**2)) + atan2(y, x)
        
        # Calculate the goal angle from [0, 0]
        motor1_goal = degrees(theta1)
        motor2_goal = -degrees(theta2)

        # Calculate the correct distance to move in order to reach the goal angle
        # given the current angle after the previous motion
        motor1_degrees = motor1_goal - startAngles[0]
        motor2_degrees = motor2_goal - startAngles[1]

        #self.sendAngles(motor1_degrees, motor2_degrees)
        trajectory.append([motor1_degrees, motor2_degrees])
        
        return [motor1_goal, motor2_goal]

    def executeTrajectory(self, trajectory):
        for angles in trajectory:
            self.sendAngles(angles[0], angles[1])

    def exit(self):
        self.server.sendTermination()
        print("Exiting server")
        time.sleep(1)




def main():
    controller = Controller()
    
    pos1 = [15, 15]
    pos2 = [-15, 15]
    
    controller.straightLine(pos1, pos2)
    controller.exit()

main()

        

