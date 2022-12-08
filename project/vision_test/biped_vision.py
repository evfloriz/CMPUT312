#!/usr/bin/env python3

'''
This program combines sensor data from analog_robot.py with
walking code from Walking.py
'''

from time import sleep
from client import Client
from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

#from GyroWalk import GyroMovement
from movement import Movement

class Robot:
    def __init__(self):
        host = "172.17.0.1"
        port = 9999
        self.client = Client(host, port)

        #self.motor1 = LargeMotor(OUTPUT_D)
        #self.motor2 = LargeMotor(OUTPUT_C)
        #self.dir = -1

        self.leftCS = ColorSensor(INPUT_3)
        self.rightCS = ColorSensor(INPUT_4)

        self.tracked_position = [0, 0]
        
        self.speed = 10

        self.angle = 0

        #self.movement = GyroMovement()
        self.movement = Movement()

        self.file = open("robot.out", "w")

    def __del__(self):
        self.client.close()
        self.file.close()

    def getCoordsFromServer(self):
        # Return true if operation should continue, false if not
    
        # Receive data from server
        data = self.client.pollData().split(',')
        if (data[0] == "EXIT"):
            return False

        # convert to float
        try:
            self.tracked_position[0] = float(data[0])
            self.tracked_position[1] = float(data[1])
        except ValueError:
            self.file.write("Error converting " + data + " to float\n")
        
        #self.file.write(str(data) + '\n');
        #self.file.write(str(self.cs1.rgb) + '\n')
        #self.file.write(str(self.cs2.rgb) + '\n')

        #print(str(self.cs1.rgb))
        #print(str(self.cs2.rgb))

        # Send done
        self.client.sendDone()

        return True
    
    
    def updateFollowAngle(self):
        # Calculate the desired angle of the camera foot to point it towards the tracked point

        # Need to calculate this properly, camera has 55deg dfov, ~45def hfov
        hfov = 45

        # image is 480 by 640
        centerX = 320
        centerY = 240

        # negative means turn left, positive means turn right
        proportionX = (self.tracked_position[0] - centerX) / centerX

        self.angle = hfov / 2 * proportionX

        # Compute estimated angle to align robot foot to center

        self.file.write(str(self.angle) + '\n')


    def moveOneCycle(self, firstCycle):
        # algorithm
        
        # while (light sensors dont detect)
            # update angles

            # lift sensor foot
            # if not first cycle:
            #   take half step forward with sensor foot
            # rotate sensor hip to point toward ball
            # lower sensor foot
            # lift nonsensor foot
            # rotate sensor hip to be in line (leaving non sensor foot)
            # take half step forward with nonsensor foot
            # lower nonsensor foot
            
        # lift sensor foot
        self.movement.liftLeft()

        # take half step forward with sensor foot if not the first cycle
        if (not firstCycle):
            self.movement.shuffleLeft()

        # rotate sensor hip to point toward ball
        self.movement.rotateLeft(self.angle)

        # lower sensor foot
        self.movement.lowerLeft()
        
        # lift nonsensor foot
        self.movement.liftRight()
        
        # rotate sensor hip to be in line (leaving non sensor foot)
        self.movement.rotateLeft(-self.angle)

        # take half step forward with nonsensor foot
        self.movement.shuffleRight()

        # lower nonsensor foot
        self.movement.lowerRight()


    def checkColorSensors(self):
        # even sensor reading threshold
        threshold = 10
        
        leftBlue = self.leftCS.rgb[2]
        rightBlue = self.rightCS.rgb[2]

        self.file.write(str(leftBlue) + " " + str(rightBlue) + '\n')

        if (leftBlue > threshold or rightBlue > threshold):
            return True

        return False
    

    def kick(self):
        self.movement.liftLeft()
        self.movement.shuffleRight()                # wind up...
        self.movement.quadShuffleLeft()             # kick!
        self.movement.doubleShuffleRight()          # return foot
        self.movement.lowerLeft()

        
def main():
    robot = Robot()

    firstCycle = True

    # main loop
    while True:

        # get coords from server
        shouldContinue = robot.getCoordsFromServer()
        if (not shouldContinue):
            break
        
        # update angle to move towards point
        robot.updateFollowAngle()

        # override follow angle with color sensors
        shouldKick = robot.checkColorSensors()
        if (shouldKick):
            robot.kick()
            break
        
        # move one cycle towards the ball
        robot.moveOneCycle(firstCycle)
        firstCycle = False

    

main()