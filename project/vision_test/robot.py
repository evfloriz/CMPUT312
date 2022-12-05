#!/usr/bin/env python3

from time import sleep
from client import Client
from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor

class Robot:
    def __init__(self):
        host = "172.17.0.1"
        port = 9999
        self.client = Client(host, port)

        self.motor1 = LargeMotor(OUTPUT_D)
        self.motor2 = LargeMotor(OUTPUT_C)
        self.dir = -1

        self.cs1 = ColorSensor(INPUT_1)
        self.cs2 = ColorSensor(INPUT_2)

        self.tracked_position = [0, 0]
        
        self.speed = 10

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
    
    
    def followPoint(self):
        # move in the direction to keep the point in the center of image
        # image is 480 by 640
        centerX = 320
        centerY = 240

        # negative means turn left, positive means turn right
        adjustX = self.tracked_position[0] - centerX
        self.file.write(str(adjustX) + '\n')

        # Adjust a max of 5 percent speed on either edge of the screen
        percent_adjust = 5
        speed_adjust = (adjustX / centerX) * percent_adjust
        
        left_speed = self.speed - speed_adjust
        right_speed = self.speed + speed_adjust

        self.move(left_speed, right_speed)


    def move(self, left_speed, right_speed):
        self.file.write("Moving at L: " + str(left_speed) + ", R:" + str(right_speed) + "\n")
        left_motor_speed = left_speed * self.dir
        right_motor_speed = right_speed * self.dir
        # run for 2 seconds
        seconds = 2
        self.motor1.on_for_seconds(SpeedPercent(left_motor_speed), seconds, brake=True, block=False)
        self.motor2.on_for_seconds(SpeedPercent(right_motor_speed), seconds, brake=True, block=False)


    def fineMove(self, left_speed, right_speed):
        self.file.write("Moving at L: " + str(left_speed) + ", R:" + str(right_speed) + "\n")
        left_motor_speed = left_speed * self.dir
        right_motor_speed = right_speed * self.dir
        # run for 0.1 seconds
        seconds = 0.1
        self.motor1.on_for_seconds(SpeedPercent(left_motor_speed), seconds, brake=True, block=False)
        self.motor2.on_for_seconds(SpeedPercent(right_motor_speed), seconds, brake=True, block=False)


    def checkColorSensors(self):
        #self.file.write(str(self.cs1.rgb) + '\n')
        #self.file.write(str(self.cs2.rgb) + '\n')
        
        # even sensor reading threshold
        threshold = 10
        
        blue1 = self.cs1.rgb[2]
        blue2 = self.cs2.rgb[2]

        self.file.write(str(blue1) + " " + str(blue2) + '\n')
        if (blue1 > 10 or blue2 > 10):
            self.stop()

            # if the two sensors are close, stop
            if (abs(blue1 - blue2) < threshold):
                return False
            else:

                # otherwise, move in the direction of the one with
                # greater value to bring them in balance
                if (blue1 > blue2):
                    self.fineMove(10, 0)
                else:
                    self.fineMove(0, 10)

        return True


            

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()

        


def main():
    robot = Robot()

    # main loop
    while True:
        # get coords from server
        shouldContinue = robot.getCoordsFromServer()
        if (not shouldContinue):
            break

        # move towards point
        robot.followPoint()

        shouldContinue = robot.checkColorSensors()
        if (not shouldContinue):
            break

        

        print("continuing")

    print("exiting")

    

main()