from startingPositions import *
from tableapi import *


def possibleMoves():
    setup_board()
    moves = []
    pieces = getPieces()
    for piece in pieces:
        row = piece[0]
        column = piece[1]
        piece = piece[2]
        if piece == "K":
            for target_row_int in range(9):
                target_row = intToLetter(target_row_int + 1)
                for target_column in range(9):
                    if isMoveLegal(row, column, target_row, str(target_column + 1), piece):
                        # print(f"{row}{column}:{target_row}{target_column}")
                        moves.append(f"{row}{column}:{target_row}{target_column + 1}")
    return moves


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
        print("Piece must move!\n")
        askForMove()
        return
    if isMoveLegal(start_square[0], start_square[1], target_square[0], target_square[1], getPiece(start_square[0], start_square[1])):
        move(start_square, target_square)
    else:
        askForMove()
        return
    return

def getScore():
    if hasWon():
        if gameData["defenderWin"]:
            return 10
        else:
            return -10
    else:
        return 0



def abminimax(depth, alpha, beta, player):



def a_comp():



def d_comp():



def makeMove(player, mode):
    if mode == 1:
        if player == 1:
            askForMove()
        else:
            d_comp()
    else:
        if player == 1:
            d_comp()
        else:
            a_comp



def setup_board():
    start_fen = normal_start
    setCurrentFen(start_fen)


def pvc():
    while True:
        choice = input("Choose team(A/D): ").upper()
        if not (choice == "A" or choice == "D"):
            print("please pick A or D")
        else:
            if choice == "A":
                order = 2
            elif choice == "D":
                order = 1
            break

    setup_board()

    if order == 1:
        current_player = 1
    elif order == 2:
        current_player = -1

    while not isGameOver():
        makeMove(current_player, 1)
        current_player *= -1

    printCurrentTable(getCurrentFen())


pvc()
