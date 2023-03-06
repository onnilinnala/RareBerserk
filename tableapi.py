from gameData import gameData


def hasWon():
    if gameData["attackerWin"] or gameData["defenderWin"]:
        return True


def setWinner(winner):
    if winner == "A":
        gameData["attackerWin"] = True
    elif winner == "D":
        gameData["defenderWin"] = True


def getCurrentFen():
    return gameData["currentPosition"]


def setCurrentFen(fen):
    gameData["currentPosition"] = fen


def getKingMoved():
    return gameData["kingMoved"]


def setKingMoved():
    gameData["kingMoved"] = True


def fenToListOf64(fen):
    board = []
    rows = fen.split("/")
    for row in rows:
        for c in row:
            if c in "123456789":
                for i in range(int(c)):
                    board.append(None)
            elif c == "k":
                board.append("K")
            elif c == "a":
                board.append("A")
            elif c == "d":
                board.append("D")
    return board


def listOf64ToFen(board):
    fen = ""
    i = 0
    for c in board:
        if i % 9 == 0 and i != 0:
            fen = fen + "/"
        if c is None:
            if len(fen) > 0:
                if fen[-1] in "12345678":
                    fen = fen[:-1] + str(int(fen[-1])+1)
                else:
                    fen = fen + "1"
            elif len(fen) == 0:
                fen = fen + "1"
        elif c == "K":
            fen = fen + "k"
        elif c == "A":
            fen = fen + "a"
        elif c == "D":
            fen = fen + "d"
        i = i + 1
    return fen


def movePiece(row, column, target_row, target_column):
    board = fenToListOf64(getCurrentFen())
    piece = board[getIndex(row, int(column))]
    board[getIndex(row, int(column))] = None
    board[getIndex(target_row, int(target_column))] = piece
    setCurrentFen(listOf64ToFen(board))


def removePiece(row, column):
    board = fenToListOf64(getCurrentFen())
    board[getIndex(row, int(column))] = None
    setCurrentFen(listOf64ToFen(board))


def getPiece(row, column):
    board = fenToListOf64(getCurrentFen())
    return board[getIndex(row, int(column))]


def getIndex(row, column):
    return (letterToInt(row)-1)*9 + column - 1


def getSquare(index):
    squares = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"]
    return squares[index]


def getPieces():
    pieces = []
    board = fenToListOf64(getCurrentFen())
    i = 0
    for square in board:
        if square == "A" or square == "D" or square == "K":
            row, column = getSquare(i)
            pieces.append(f"{row}{column}{square.upper()}")
        i = i + 1
    return pieces


def move(start_square, target_square):
    # Set variables from squares
    row, column, target_row, target_column = start_square[0], start_square[1], target_square[0], target_square[1]

    # Get piece. Existence of piece is checked in askForMove()
    piece = getPiece(row, column)

    # Check if move is legal (more in isMoveLegal())
    if isMoveLegal(row, column, target_row, target_column, piece):
        # If Move is legal move the piece
        movePiece(row, column, target_row, target_column)

        # Check if king is trapped
        if checkKingTrapped():
            printCurrentTable(getCurrentFen())
            defendersWin()

        # If piece is king and start_square is the throne set kingMoved to True
        if piece == "K":
            if start_square == "E5":
                setKingMoved()
                checkThroneKills()
            elif target_square == "A1" or target_square == "A9" or target_square == "I1" or target_square == "I9":
                printCurrentTable(getCurrentFen())
                attackersWin()

        # Do the killing :D
        left, right, up, down = checkForKillsAround(row, column, target_row, target_column, piece, False)
        afterMoveKill(left, right, up, down, target_row, target_column)

        # Print current table
        printCurrentTable(getCurrentFen())
        return

    # If move is illegal return to askForMove()
    else:
        return


# Transform row letter to number for calculating
def letterToInt(row):
    if row == "A":
        return 1
    elif row == "B":
        return 2
    elif row == "C":
        return 3
    elif row == "D":
        return 4
    elif row == "E":
        return 5
    elif row == "F":
        return 6
    elif row == "G":
        return 7
    elif row == "H":
        return 8
    elif row == "I":
        return 9
    else:
        return 0


# Transform number to row letter after calculating
def intToLetter(row_int):
    if row_int == 1:
        return "A"
    elif row_int == 2:
        return "B"
    elif row_int == 3:
        return "C"
    elif row_int == 4:
        return "D"
    elif row_int == 5:
        return "E"
    elif row_int == 6:
        return "F"
    elif row_int == 7:
        return "G"
    elif row_int == 8:
        return "H"
    elif row_int == 9:
        return "I"
    else:
        return


def printCurrentTable(fen):
    board = "    |1|2|3|4|5|6|7|8|9|\n"
    current_row = 1
    for row in fen.split('/'):
        row_letter = intToLetter(current_row)
        b_row = f"({row_letter}) |"
        for c in row:
            if c == ' ':
                break
            elif c == "d":
                b_row = b_row + 'D|'
            elif c == "a":
                b_row = b_row + 'A|'
            elif c == "k":
                b_row = b_row + 'K|'
            elif c in '123456789':
                for i in range(int(c)):
                    b_row = b_row + ' |'
        # Draw X's if the squares are empty
        if current_row == 1:
            if b_row[5] == " ":
                b_row = b_row[:5] + "X" + b_row[6:]
            if b_row[21] == " ":
                b_row = b_row[:21] + "X" + b_row[22:]
        if current_row == 5:
            if b_row[13] == " ":
                b_row = b_row[:13] + "X" + b_row[14:]
        if current_row == 9:
            if b_row[5] == " ":
                b_row = b_row[:5] + "X" + b_row[6:]
            if b_row[21] == " ":
                b_row = b_row[:21] + "X" + b_row[22:]
        board = board + b_row + "\n"
        current_row = current_row + 1
    print(board)


# Check if row is clear until target square
def checkRow(row, column, target_column):
    # If going right. Ex. 1 -> 6
    if int(column) < int(target_column):
        steps = int(target_column) - int(column)
        for step in range(steps):
            step = step + 1
            if getPiece(row, str(int(column)+step)) is None:
                pass
            else:
                return False
        return True

    # If going left. Ex. 6 -> 1
    elif int(column) > int(target_column):
        steps = int(column) - int(target_column)
        for step in range(steps):
            step = step + 1
            if getPiece(row, str(int(column)-step)) is None:
                pass
            else:
                return False
        return True


# Check if column is clear until target square
def checkColumn(column, row, target_row):
    # If going down. Ex. A -> F
    if letterToInt(row) < letterToInt(target_row):
        steps = letterToInt(target_row) - letterToInt(row)
        for step in range(steps):
            step = step + 1
            if getPiece(intToLetter(letterToInt(row) + step), column) is None:
                pass
            else:
                return False
        return True

    # If going up. Ex. F -> A
    elif letterToInt(row) > letterToInt(target_row):
        steps = letterToInt(row) - letterToInt(target_row)
        for step in range(steps):
            step = step + 1
            if getPiece(intToLetter(letterToInt(row) - step), column) is None:
                pass
            else:
                return False
        return True


# Check if selected square is valid. Check_type is either Start or Target.
def checkSquareValidity(square, check_type):
    # Check if square input is 2 characters Ex. A5
    if len(square) == 2:

        # Check if first character is in range A-I
        if square[0] == "A" or square[0] == "B" or square[0] == "C" or square[0] == "D" or square[0] == "E" or square[0] == "F" or square[0] == "G" or square[0] == "H" or square[0] == "I":

            # Check if second character is in range 1-9
            if square[1] == "1" or square[1] == "2" or square[1] == "3" or square[1] == "4" or square[1] == "5" or square[1] == "6" or square[1] == "7" or square[1] == "8" or square[1] == "9":

                # If type is start check that the square holds a piece
                if check_type == "Start":
                    if getPiece(square[0], square[1]):
                        pass
                    else:
                        return False

                # If type is target check that the square is empty
                elif check_type == "Target":
                    if getPiece(square[0], square[1]) is None:
                        pass
                    else:
                        return False
            else:
                return False
        else:
            return False
    else:
        return False
    return True


# Make the kills after the move is done. Variables come from move() and checkKillsAround()
def afterMoveKill(left, right, up, down, target_row, target_column):
    if left:
        removePiece(target_row, str(int(target_column) - 1))
    if right:
        removePiece(target_row, str(int(target_column) + 1))
    if up:
        removePiece(intToLetter(letterToInt(target_row) - 1), target_column)
    if down:
        removePiece(intToLetter(letterToInt(target_row) + 1), target_column)


# Check if surrounding squares are out of bounds
def outOfBoundsCheck(target_row, target_column):

    # Set the variables to False as a default
    left_oob, right_oob, up_oob, down_oob = False, False, False, False

    # If row is A or as an integer 1 the square on top is out of bounds
    if letterToInt(target_row) == 1:
        up_oob = True

    # If row is I or as an integer 9 the square below is out of bounds
    if letterToInt(target_row) == 9:
        down_oob = True

    # If column is 1 the square on the left would be 0 so it is out of bounds
    if target_column == "1":
        left_oob = True

    # If column is 9 the square on the right would be 10 so it is out of bounds
    if target_column == "9":
        right_oob = True

    return left_oob, right_oob, up_oob, down_oob


# Check for enemies and killSquares around a selected square
def checkForKillSquaresAround(target_row, target_column, piece):
    # Set the variables to False as a default
    left, right, up, down = False, False, False, False

    # Check if the directions are out of bounds to prevent errors
    lo, ro, uo, do = outOfBoundsCheck(target_row, target_column)

    # If left isn't out of bounds
    if not lo:
        # Check if the square on the left is either an enemy or a killSquare(corner or throne)
        if isEnemyOrKillSquare(target_row, str(int(target_column) - 1), piece):
            left = True

    # If right isn't out of bounds
    if not ro:
        # Check if the square on the right is either an enemy or a killSquare(corner or throne)
        if isEnemyOrKillSquare(target_row, str(int(target_column)), piece):
            right = True

    # If up isn't out of bounds
    if not uo:
        # Check if the square on top is either an enemy or a killSquare(corner or throne)
        if isEnemyOrKillSquare(intToLetter(letterToInt(target_row) - 1), target_column, piece):
            up = True

    # If down isn't out of bounds
    if not do:
        # Check if the square below is either an enemy or a killSquare(corner or throne)
        if isEnemyOrKillSquare(intToLetter(letterToInt(target_row) + 1), target_column, piece):
            down = True

    return left, right, up, down, lo, ro, uo, do


# Play move virtually (Same as movePiece() but is used before the actual move for clarity)
def playVirtualMove(row, column, target_row, target_column):
    movePiece(row, column, target_row, target_column)


# Undo a Virtual Move (Opposite of playVirtualMove() used so same order of variables can be used)
def undoVirtualMove(row, column, target_row, target_column):
    movePiece(target_row, target_column, row, column)


# Check if piece would die if it entered the target square
def checkForDeath(row, column, piece):
    # Get surrounding killSquares
    left, right, up, down, lo, ro, uo, do = checkForKillSquaresAround(row, column, piece)

    # If piece isn't King
    if piece != "K":

        # If the square on the left and the square on the right are both killSquares return True for Kill
        if left and right:
            return True

        # If the square on top and the square below are both killSquares return True for Kill
        if up and down:
            return True

        # If two opposite squares aren't killSquares return False for Kill
        return False

    # If piece is King
    elif piece == "K":

        # If all directions are blocked or out of bounds
        if left and right and up and down:
            return True

        # If all directions are blocked or out of bounds
        elif lo and right and up and down:
            return True

        # If all directions are blocked or out of bounds
        elif left and ro and up and down:
            return True

        # If all directions are blocked or out of bounds
        elif left and right and uo and down:
            return True

        # If all directions are blocked or out of bounds
        elif left and right and up and do:
            return True

        # If one or more direction is not occupied by an enemy and not out of bounds
        return False
    return False


# Check if there are kills around the target piece. Virtual variable is used for moves that are part of the legality check
def checkForKillsAround(row, column, target_row, target_column, piece, virtual):
    # Set the default of the variables to False
    left, right, up, down = False, False, False, False

    # Check if the directions are out of bounds to prevent errors
    lo, ro, uo, do = outOfBoundsCheck(target_row, target_column)

    # If move isn't an actual move but apart of legality check play a virtual move to check kills correctly
    if virtual:
        playVirtualMove(row, column, target_row, target_column)

    # If left isn't out of bounds
    if not lo:
        # If the square on the left has an enemy piece
        if getPiece(target_row, str(int(target_column) - 1)) == getEnemy(piece):
            # If the enemy piece on the left will die after the move
            if checkForDeath(target_row, str(int(target_column) - 1), getEnemy(piece)):
                left = True

    # If right isn't out of bounds
    if not ro:
        # If the square on the right has an enemy piece
        if getPiece(target_row, str(int(target_column) + 1)) == getEnemy(piece):
            # If the enemy piece on the right will die after the move
            if checkForDeath(target_row, str(int(target_column) + 1), getEnemy(piece)):
                right = True

    # If up isn't out of bounds
    if not uo:
        # If the square on top has an enemy piece
        if getPiece(intToLetter(letterToInt(target_row) - 1), target_column) == getEnemy(piece):
            # If the enemy piece on top will die after the move
            if checkForDeath(intToLetter(letterToInt(target_row) - 1), target_column, getEnemy(piece)):
                up = True

    # If down isn't out of bounds
    if not do:
        # If the square below has an enemy piece
        if getPiece(intToLetter(letterToInt(target_row) + 1), target_column) == getEnemy(piece):
            # If the enemy piece below will die after the move
            if checkForDeath(intToLetter(letterToInt(target_row) + 1), target_column, getEnemy(piece)):
                down = True

    # If move isn't an actual move, but apart of legality check, undo the virtual move done previously
    if virtual:
        undoVirtualMove(row, column, target_row, target_column)

    # Return pieces that will die
    return left, right, up, down


def checkForKillsAroundThrone():
    target_row = "E"
    target_column = "5"

    # Set the default of the variables to False
    left, right, up, down = False, False, False, False

    # If the square on the left has an enemy piece
    if getPiece(target_row, str(int(target_column) - 1)):
        # If the enemy piece on the left will die after the move
        if checkForDeath(target_row, str(int(target_column) - 1), "A") or checkForDeath(target_row, str(int(target_column) - 1), "D"):
            left = True

    # If the square on the right has an enemy piece
    if getPiece(target_row, str(int(target_column) + 1)):
        # If the enemy piece on the right will die after the move
        if checkForDeath(target_row, str(int(target_column) + 1), "A") or checkForDeath(target_row, str(int(target_column) + 1), "D"):
            right = True

    # If the square on top has an enemy piece
    if getPiece(intToLetter(letterToInt(target_row) - 1), target_column):
        # If the enemy piece on top will die after the move
        if checkForDeath(intToLetter(letterToInt(target_row) - 1), target_column, "A") or checkForDeath(intToLetter(letterToInt(target_row) - 1), target_column, "D"):
            up = True

    # If the square below has an enemy piece
    if getPiece(intToLetter(letterToInt(target_row) + 1), target_column):
        # If the enemy piece below will die after the move
        if checkForDeath(intToLetter(letterToInt(target_row) + 1), target_column, "A") or checkForDeath(intToLetter(letterToInt(target_row) + 1), target_column, "D"):
            down = True

    # Return pieces that will die
    return left, right, up, down


# Check whether the piece moves along a row or a column
def rowOrColumn(row, column, target_row, target_column):
    # If start_row and target_row are the same the piece moves along the row
    if row == target_row:
        return 1

    # If start_column and target_column are the same the piece moves along the column
    elif column == target_column:
        return 2


# Check if given move is legal
def isMoveLegal(row, column, target_row, target_column, piece):
    # Checking start piece and occupancy of target square is done in checkSquareValidity()
    # If target is The Throne check if piece is king
    if target_row == "E" and target_column == "5":
        if piece != "K":
            # print("Only king can enter the center square!")
            return False
    # If target square is a corner check if piece is king
    elif target_row == "A" or target_row == "I":
        if target_column == "1" or target_column == "9":
            if piece != "K":
                # print("Only king can enter a corner!")
                return False
    # Check whether the piece moves along a row(letters) or a column(numbers)
    if rowOrColumn(row, column, target_row, target_column) == 1:
        # If piece moves along a row(letters) check occupancy of squares till target square
        if not checkRow(row, column, target_column):
            # print("Can't go through other pieces!")
            return False
    # Check whether the piece moves along a row(letters) or a column(numbers)
    elif rowOrColumn(row, column, target_row, target_column) == 2:
        # If piece moves along a column(numbers) check occupancy of squares till target square
        if not checkColumn(column, row, target_row):
            # print("Can't go through other pieces!")
            return False
    # If piece doesnt move along a row or a column the piece isn't moving in a straight line
    else:
        # print("All pieces must move in a straight line!")
        return False
    # Check if the piece will die at the target square
    if checkForDeath(target_row, target_column, piece):
        # If the piece dies at the target square check if it can kill a piece there making the move legal
        if not any(checkForKillsAround(row, column, target_row, target_column, piece, True)):
            #print("The target square would be an instant kill!")
            return False
    return True


# Get enemy of given piece. Used for clarity
def getEnemy(piece):
    if piece == "A" or piece == "K":
        enemy = "D"
    elif piece == "D":
        enemy = "A"
    return enemy


# Check if given square is an enemy or a killSquare
def isEnemyOrKillSquare(target_row, target_column, piece):
    if getPiece(target_row, target_column) == getEnemy(piece) or isKillSquare(target_row, target_column):
        return True


# Check if given square is a corner or The Throne and if Throne check if king has moved
def isKillSquare(target_row, target_column):
    if target_row == "A" or target_row == "I":
        if target_column == "1" or target_column == "9":
            return True
    elif target_row == "E" and target_column == "5":
        if getKingMoved():
            return True
    return False


def checkThroneKills():
    #print("Checking Throne kills!")
    left, right, up, down = checkForKillsAroundThrone()
    #print(left, right, up, down)
    afterMoveKill(left, right, up, down, "E", "5")


def checkKingTrapped():
    king_square = getKingSquare()
    if checkForDeath(king_square[0], king_square[1], "K"):
        return True
    return False


def getKingSquare():
    board = fenToListOf64(getCurrentFen())
    index = board.index("K")
    column = (index + 1) % 9
    row = intToLetter(int((index - column + 1) / 9)+1)
    return row, str(column)


def attackersWin():
    #print("Attackers win!")
    setWinner("A")


def defendersWin():
    #print("Defenders win!")
    setWinner("D")


def isGameOver():
    if hasWon():
        return True
    return False