#!/usr/bin/env python3
from Walking import Movement
from time import sleep
from GyroWalk import GyroMovement

#robot2 = Movement(100)
robot = GyroMovement(30)

#robot.liftRight()
robot.firstStepRight()
robot.stepLeft()
robot.stepRight()
robot.liftLeft()
robot.halfStepLeft()
#robot.lowerLeft()


#robot2.fullDance()

#robot2.walk(10)



sleep(5)