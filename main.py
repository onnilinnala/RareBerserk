from startingPositions import *
from tableapi import *


def start():
    start_fen = normal_start
    setCurrentFen(start_fen)
    printCurrentTable(getCurrentFen())
    askForMove()


def askForMove():
    start_square = input("Select piece: ").upper()
    target_square = input("Target square: ").upper()
    if not checkSquareValidity(start_square, "Start"):
        print("Start")
        print("Invalid square selected!\n")
        askForMove()
        return
    if not checkSquareValidity(target_square, "Target"):
        print("Target")
        print("Invalid square selected!\n")
        askForMove()
        return
    if target_square == start_square:
        print("No move selected!\n")
        askForMove()
        return
    move(start_square, target_square)
    askForMove()
    return


start()
