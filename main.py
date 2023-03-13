from startingPositions import *
from tableapi import *


def init():
    setPosition(normal_start)
    printPosition(getPosition())
    start()


def start():
    while True:
        try:
            start_index = getIndex(input("Select piece: ").upper())
            break
        except Exception as e:
            print(e)
    while True:
        try:
            target_index = getIndex(input("Target square: ").upper())
            break
        except Exception as e:
            print(e)
    move(start_index, target_index)
    start()
    return


init()
