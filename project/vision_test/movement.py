'''
This class holds the movement primitives for the biped
'''

import hello
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent

class Movement:
    def __init__(self):
        self.leftAnkle = LargeMotor(OUTPUT_D)
        self.rightAnkle = LargeMotor(OUTPUT_C)
        self.leftHip = LargeMotor(OUTPUT_B)
        self.rightHip = LargeMotor(OUTPUT_A)

        self.last_dir = {
            self.leftAnkle: 0,
            self.rightAnkle: 0,
            self.leftHip: 0,
            self.rightHip: 0
        }

    def compensate(self, motor):
        # small movement to balance out changes in direction
        angle = 10 * 5 * self.last_dir[motor] * -1
        motor.on_for_degrees(SpeedPercent(20), angle)

    def checkLastDir(self, motor, dirToMove):
        dirToMove = int(dirToMove)
        if (self.last_dir[motor] != dirToMove):
            self.compensate(motor)

        self.last_dir[motor] = dirToMove
    
    def liftRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        self.rightAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(10), 120, brake=True, block=True)

        sleep(1)
        return True

    def lowerRight(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        self.leftAnkle.on_for_degrees(SpeedPercent(10), -120, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)

        sleep(1)
        return True

    def liftLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        self.leftAnkle.on_for_degrees(SpeedPercent(20), -220, brake=True, block=False)
        self.rightAnkle.on_for_degrees(SpeedPercent(10), 120, brake=True, block=True)
        
        sleep(1)
        return True

    def lowerLeft(self):
        self.leftHip.off(brake=True)
        self.rightHip.off(brake=True)

        self.rightAnkle.on_for_degrees(SpeedPercent(10), -120, brake=True, block=False)
        self.leftAnkle.on_for_degrees(SpeedPercent(20), 220, brake=True, block=True)

        sleep(1)
        return True

    def shuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.checkLastDir(self.rightHip, -1)
        self.checkLastDir(self.leftHip, 1)
        
        self.rightHip.on_for_degrees(SpeedPercent(15), -20*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), 20*5, brake=True, block=True)

        sleep(1)
        return True

    def shuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.checkLastDir(self.rightHip, 1)
        self.checkLastDir(self.leftHip, -1)

        self.rightHip.on_for_degrees(SpeedPercent(15), 20*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(15), -20*5, brake=True, block=True)

        sleep(1)
        return True

    def doubleShuffleRight(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.checkLastDir(self.rightHip, -1)
        self.checkLastDir(self.leftHip, 1)
        
        self.rightHip.on_for_degrees(SpeedPercent(30), -40*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(30), 40*5, brake=True, block=True)

        sleep(1)
        return True

    def doubleShuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.checkLastDir(self.rightHip, 1)
        self.checkLastDir(self.leftHip, -1)

        self.rightHip.on_for_degrees(SpeedPercent(30), 40*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(30), -40*5, brake=True, block=True)

        sleep(1)
        return True

    def quadShuffleLeft(self):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)

        self.checkLastDir(self.rightHip, 1)
        self.checkLastDir(self.leftHip, -1)

        self.rightHip.on_for_degrees(SpeedPercent(30), 80*5, brake=True, block=False)
        self.leftHip.on_for_degrees(SpeedPercent(30), -80*5, brake=True, block=True)
        
        sleep(1)
        return True


    def rotateLeft(self, angle):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.rightHip.off(brake=True)

        dir = angle / abs(angle)
        hello.debug_print(dir)
        self.checkLastDir(self.leftHip, dir)

        self.leftHip.on_for_degrees(SpeedPercent(15), angle*5, brake=True, block=True)

        sleep(1)
        return True

    def rotateRight(self, angle):
        self.leftAnkle.off(brake=True)
        self.rightAnkle.off(brake=True)
        self.leftHip.off(brake=True)

        dir = angle / abs(angle)
        hello.debug_print(dir)
        self.checkLastDir(self.rightHip, dir)

        self.rightHip.on_for_degrees(SpeedPercent(15), angle*5, brake=True, block=True)

        sleep(1)
        return True

    def stepRight(self):
        self.liftRight()
        self.shuffleRight()
        self.shuffleRight()
        self.lowerRight()
        return True

    def stepLeft(self):
        self.liftLeft()
        self.shuffleLeft()
        self.shuffleLeft()
        self.lowerLeft()
        return True

    def halfStepRight(self):
        self.liftRight()
        self.shuffleRight()
        self.lowerRight()
        return True

    def halfStepLeft(self):
        self.liftLeft()
        self.shuffleLeft()
        self.lowerLeft()
        return True
