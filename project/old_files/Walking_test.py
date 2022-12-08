#!/usr/bin/env python3

from Walking import Movement

def main():
    distance = 300
    speed = 10
    fullStepSize = 50
    walking = Movement(distance, speed, fullStepSize)

    walking.walk()


main()
