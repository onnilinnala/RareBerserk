from main_table import main_table as table


def changePiece(row, column, piece):
    table[row][column]["Piece"] = piece


def changeKill(row, column, kill):
    table[row][column]["KillSquare"] = kill


def getData(row, column, data_type):
    return table[row][column][data_type]


def move(start_square, target_square):
    # Set variables from squares
    row, column, target_row, target_column = start_square[0], start_square[1], target_square[0], target_square[1]

    # Get piece. Existence of piece is checked in askForMove()
    piece = getData(row, column, "Piece")

    # Check if move is legal (more in isMoveLegal())
    if isMoveLegal(row, column, target_row, target_column, piece):
        # If Move is legal move the piece
        movePiece(row, column, target_row, target_column)

        # Do the killing :D
        left, right, up, down = checkForKillsAround(row, column, target_row, target_column, piece, False)
        afterMoveKill(left, right, up, down, target_row, target_column)

        # Print current table
        printCurrentTable()
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


# Print current table
def printCurrentTable():
    # First line to print the numbers
    table_txt = ""
    table_txt = table_txt + "    |1|2|3|4|5|6|7|8|9|\n"

    # For every row in the table add a row letter
    for row in table:
        row_txt = f"({row}) |"

        # For every column in every row check for piece and add a letter corresponding to the data of the square.
        for column in range(9):
            if table[row][str(column + 1)]["Piece"] is None:
                if table[row][str(column + 1)]["KillSquare"]:
                    row_txt = row_txt + f'X|'
                else:
                    row_txt = row_txt + f' |'
            elif table[row][str(column + 1)]["Piece"] == "1":
                row_txt = row_txt + f'D|'
            elif table[row][str(column + 1)]["Piece"] == "2":
                row_txt = row_txt + f'A|'
            elif table[row][str(column + 1)]["Piece"] == "3":
                row_txt = row_txt + f'K|'
        table_txt = table_txt + row_txt + "\n"
    print(table_txt)


# Check if row is clear until target square
def checkRow(row, column, target_column):
    # If going right. Ex. 1 -> 6
    if int(column) < int(target_column):
        steps = int(target_column) - int(column)
        for step in range(steps):
            step = step + 1
            if getData(row, str(int(column)+step), "Piece") is None:
                pass
            else:
                return False
        return True

    # If going left. Ex. 6 -> 1
    elif int(column) > int(target_column):
        steps = int(column) - int(target_column)
        for step in range(steps):
            step = step + 1
            if getData(row, str(int(column)-step), "Piece") is None:
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
            if table[intToLetter(letterToInt(row) + step)][column]["Piece"] is None:
                pass
            else:
                return False
        return True

    # If going up. Ex. F -> A
    elif letterToInt(row) > letterToInt(target_row):
        steps = letterToInt(row) - letterToInt(target_row)
        for step in range(steps):
            step = step + 1
            if table[intToLetter(letterToInt(row) - step)][column]["Piece"] is None:
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
                    if getData(square[0], square[1], "Piece"):
                        pass
                    else:
                        return False

                # If type is target check that the square is empty
                elif check_type == "Target":
                    if not getData(square[0], square[1], "Piece"):
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
        changePiece(target_row, str(int(target_column) - 1), None)
    if right:
        changePiece(target_row, str(int(target_column) + 1), None)
    if up:
        changePiece(intToLetter(letterToInt(target_row) - 1), target_column, None)
    if down:
        changePiece(intToLetter(letterToInt(target_row) + 1), target_column, None)


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
        if isKillSquare(target_row, str(int(target_column) - 1), piece):
            left = True

    # If right isn't out of bounds
    if not ro:
        # Check if the square on the right is either an enemy or a killSquare(corner or throne)
        if isKillSquare(target_row, str(int(target_column) + 1), piece):
            right = True

    # If up isn't out of bounds
    if not uo:
        # Check if the square on top is either an enemy or a killSquare(corner or throne)
        if isKillSquare(intToLetter(letterToInt(target_row) - 1), target_column, piece):
            up = True

    # If down isn't out of bounds
    if not do:
        # Check if the square below is either an enemy or a killSquare(corner or throne)
        if isKillSquare(intToLetter(letterToInt(target_row) + 1), target_column, piece):
            down = True

    return left, right, up, down


# Play move virtually (Same as movePiece() but is used before the actual move for clarity)
def playVirtualMove(row, column, target_row, target_column):
    piece = getData(row, column, "Piece")
    changePiece(row, column, None)
    changePiece(target_row, target_column, piece)


# Undo a Virtual Move (Opposite of playVirtualMove() used so same order of variables can be used)
def undoVirtualMove(row, column, target_row, target_column):
    piece = getData(target_row, target_column, "Piece")
    changePiece(target_row, target_column, None)
    changePiece(row, column, piece)


# Check if piece would die if it entered the target square
def checkForDeath(row, column, piece):
    # Get surrounding killSquares
    left, right, up, down = checkForKillSquaresAround(row, column, piece)

    # If the square on the left and the square on the right are both killSquares return True for Kill
    if left and right:
        return True

    # If the square on top and the square below are both killSquares return True for Kill
    if up and down:
        return True

    # If two opposite squares aren't killSquares return False for Kill
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
        if getData(target_row, str(int(target_column) - 1), "Piece") == getEnemy(piece):
            # If the enemy piece on the left will die after the move
            if checkForDeath(target_row, str(int(target_column) - 1), getEnemy(piece)):
                left = True

    # If right isn't out of bounds
    if not ro:
        # If the square on the right has an enemy piece
        if getData(target_row, str(int(target_column) + 1), "Piece") == getEnemy(piece):
            # If the enemy piece on the right will die after the move
            if checkForDeath(target_row, str(int(target_column) + 1), getEnemy(piece)):
                right = True

    # If up isn't out of bounds
    if not uo:
        # If the square on top has an enemy piece
        if getData(intToLetter(letterToInt(target_row) - 1), target_column, "Piece") == getEnemy(piece):
            # If the enemy piece on top will die after the move
            if checkForDeath(intToLetter(letterToInt(target_row) - 1), target_column, getEnemy(piece)):
                up = True

    # If down isn't out of bounds
    if not do:
        # If the square below has an enemy piece
        if getData(intToLetter(letterToInt(target_row) + 1), target_column, "Piece") == getEnemy(piece):
            # If the enemy piece below will die after the move
            if checkForDeath(intToLetter(letterToInt(target_row) + 1), target_column, getEnemy(piece)):
                down = True

    # If move isn't an actual move, but apart of legality check, undo the virtual move done previously
    if virtual:
        undoVirtualMove(row, column, target_row, target_column)

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


# Move the piece
def movePiece(row, column, target_row, target_column):
    # Get piece from start_square
    piece = getData(row, column, "Piece")

    # Change start_square to None
    changePiece(row, column, None)

    # Change target_square to Piece
    changePiece(target_row, target_column, piece)


# Check if given move is legal
def isMoveLegal(row, column, target_row, target_column, piece):
    # Checking start piece and occupancy of target square is done in checkSquareValidity()
    # If target is The Throne check if piece is king
    if target_row == "E" and target_column == "5":
        if piece != "3":
            print("Only king can enter the center square!")
            return
    # If target square is a corner check if piece is king
    elif target_row == "A" or target_row == "I":
        if target_column == "1" or target_column == "9":
            if piece != "3":
                print("Only king can enter a corner!")
                return
    # Check whether the piece moves along a row(letters) or a column(numbers)
    if rowOrColumn(row, column, target_row, target_column) == 1:
        # If piece moves along a row(letters) check occupancy of squares till target square
        if not checkRow(row, column, target_column):
            print("Can't go through other pieces!")
            return False
    # Check whether the piece moves along a row(letters) or a column(numbers)
    elif rowOrColumn(row, column, target_row, target_column) == 2:
        # If piece moves along a column(numbers) check occupancy of squares till target square
        if not checkColumn(column, row, target_row):
            print("Can't go through other pieces!")
            return False
    # If piece doesnt move along a row or a column the piece isn't moving in a straight line
    else:
        print("All pieces must move in a straight line!")
        return False
    # Check if the piece will die at the target square
    if checkForDeath(target_row, target_column, piece):
        # If the piece dies at the target square check if it can kill a piece there making the move legal
        if not any(checkForKillsAround(row, column, target_row, target_column, piece, True)):
            print("The target square would be an instant kill!")
            return False
    return True


# Get enemy of given piece. Used for clarity
def getEnemy(piece):
    if piece == "1":
        enemy = "2"
    elif piece == "2":
        enemy = "1"
    return enemy


# Check if given square is an enemy or a killSquare
def isKillSquare(target_row, target_column, piece):
    if getData(target_row, target_column, "Piece") == getEnemy(piece) or getData(target_row, target_column, "KillSquare"):
        return True
