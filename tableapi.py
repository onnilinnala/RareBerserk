from main_table import main_table as table


def changePiece(row, column, piece):
    table[row][column]["Piece"] = piece


def changeKill(row, column, kill):
    table[row][column]["KillSquare"] = kill


def getData(row, column, dataType):
    return table[row][column][dataType]


def move(start_square, target_square):
    row, column = start_square[0], start_square[1]
    target_row, target_column = target_square[0], target_square[1]
    if not getData(row, column, "Piece"):
        return
    piece = getData(row, column, "Piece")
    if isMoveLegal(row, column, target_row, target_column, piece):
        movePiece(row, column, target_row, target_column, piece)
        left, right, up, down = checkForKillAround(target_row, target_column, piece)
        if left:
            changePiece(target_row, str(int(target_column)-1), None)
        if right:
            changePiece(target_row, str(int(target_column)+1), None)
        if up:
            changePiece(intToLetter(letterToInt(target_row)-1), target_column, None)
        if down:
            changePiece(intToLetter(letterToInt(target_row)+1), target_column, None)
        printCurrentTable()


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


def intToLetter(int):
    if int == 1:
        return "A"
    elif int == 2:
        return "B"
    elif int == 3:
        return "C"
    elif int == 4:
        return "D"
    elif int == 5:
        return "E"
    elif int == 6:
        return "F"
    elif int == 7:
        return "G"
    elif int == 8:
        return "H"
    elif int == 9:
        return "I"
    else:
        return


def printCurrentTable():
    print("    |1|2|3|4|5|6|7|8|9|")
    for row in table:
        row_txt = f"({row}) |"
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
        print(row_txt)


def checkRow(row, column, target_column):
    # Ex. 1 -> 6
    if int(column) < int(target_column):
        steps = int(target_column) - int(column)
        for step in range(steps):
            step = step + 1
            if getData(row, str(int(column)+step), "Piece") is None:
                pass
            else:
                return False
        return True
    # Ex. 6 -> 1
    elif int(column) > int(target_column):
        steps = int(column) - int(target_column)
        for step in range(steps):
            step = step + 1
            if getData(row, str(int(column)-step), "Piece") is None:
                pass
            else:
                print(row)
                print(str(int(column)-step))
                return False
        return True


def checkColumn(column, row, target_row):
    # Ex. A -> F
    if letterToInt(row) < letterToInt(target_row):
        steps = letterToInt(target_row) - letterToInt(row)
        for step in range(steps):
            step = step + 1
            if table[intToLetter(letterToInt(row) + step)][column]["Piece"] is None:
                pass
            else:
                return False
        return True
    elif letterToInt(row) > letterToInt(target_row):
        steps = letterToInt(row) - letterToInt(target_row)
        for step in range(steps):
            step = step + 1
            if table[intToLetter(letterToInt(row) - step)][column]["Piece"] is None:
                pass
            else:
                return False
        return True


def checkSquareValidity(square):
    if len(square) == 2:
        if square[0] == "A" or square[0] == "B" or square[0] == "C" or square[0] == "D" or square[0] == "E" or square[0] == "F" or square[0] == "G" or square[0] == "H" or square[0] == "I":
            if square[1] == "1" or square[1] == "2" or square[1] == "3" or square[1] == "4" or square[1] == "5" or square[1] == "6" or square[1] == "7" or square[1] == "8" or square[1] == "9":
                pass
            else:
                return False
        else:
            return False
    else:
        return False
    return True


def outOfBoundsCheck(target_row, target_column):
    left_oob, right_oob, up_oob, down_oob = False, False, False, False
    if letterToInt(target_row) == 1:
        up_oob = True
    if letterToInt(target_row) == 9:
        down_oob = True
    if target_column == "1":
        left_oob = True
    if target_column == "9":
        right_oob = True
    return left_oob, right_oob, up_oob, down_oob


def checkForKillSquaresAround(target_row, target_column, piece):
    left, right, up, down = False, False, False, False
    lo, ro, uo, do = outOfBoundsCheck(target_row, target_column)
    if not lo:
        if isKillSquare(target_row, str(int(target_column) - 1), piece):
            left = True
    if not ro:
        if isKillSquare(target_row, str(int(target_column) + 1), piece):
            right = True
    if not uo:
        if isKillSquare(intToLetter(letterToInt(target_row) - 1), target_column, piece):
            up = True
    if not do:
        if isKillSquare(intToLetter(letterToInt(target_row) + 1), target_column, piece):
            down = True
    return left, right, up, down


def playVirtualMove(row, column, target_row, target_column):
    piece = getData(row, column, "Piece")
    changePiece(row, column, None)
    changePiece(target_row, target_column, piece)


def undoVirtualMove(row, column, target_row, target_column):
    piece = getData(row, column, "Piece")
    changePiece(target_row, target_column, None)
    changePiece(row, column, piece)


def checkForDeath(row, column, piece):
    if piece == "1":
        piece = "2"
    elif piece == "2":
        piece = "1"
    left, right, up, down = checkForKillSquaresAround(row, column, piece)
    if left and right:
        return True
    if up and down:
        return True
    return False


def checkForKill(row, column, piece):



def basicLegalityCheck(row, column, target_row, target_column, piece):
    if getData(row, column, "Piece") is None:
        print("Failed StartPieceCheck!")
        return
    if getData(target_row, target_column, "Piece") is not None:
        print("Failed TargetPieceCheck!")
        return
    if target_row == "E" and target_column == "5":
        if piece != "3":
            print("Only king can enter the center square!")
            return
    elif target_row == "A" or target_row == "I":
        if target_column == "1" or target_column == "9":
            if piece != "3":
                print("Only king can enter the corners!")
                return
    if rowOrColumn(row, column, target_row, target_column) == 1:
        if not checkRow(row, column, target_column):
            print("Failed checkRow!")
            return False
    elif rowOrColumn(row, column, target_row, target_column) == 2:
        if not checkColumn(column, row, target_row):
            print("Failed checkColumn!")
            return False
    else:
        print("Must move in straight lines!")
        return False
    return True


def rowOrColumn(row, column, target_row, target_column):
    if row == target_row:
        return 1
    elif column == target_column:
        return 2
    return 0


def movePiece(row, column, target_row, target_column, piece):
    changePiece(row, column, None)
    changePiece(target_row, target_column, piece)


def isMoveLegal(row, column, target_row, target_column, piece):
    if not basicLegalityCheck(row, column, target_row, target_column, piece):
        print("Failed basicLegalityCheck!")
        return False
    if checkForDeath(target_row, target_column, piece):
        playVirtualMove(row, column, target_row, target_column)
        if not any(checkForKillAround(target_row, target_column, piece)):
            print("Failed checkForKill!")
            undoVirtualMove(row, column, target_row, target_column)
            return False
    return True


def checkForEnemies(target_row, target_column, piece):
    if piece == "1":
        enemy = "2"
    elif piece == "2":
        enemy = "1"


def getEnemy(piece):
    if piece == "1":
        enemy = "2"
    elif piece == "2":
        enemy = "1"
    return enemy


def isKillSquare(target_row, target_column, piece):
    if getData(target_row, target_column, "Piece") == getEnemy(piece) or getData(target_row, target_column, "KillSquare"):
        return True
"""
CheckForDeath tarkistaa onko kohderuutu kahden vastustajan nappulan tai vastustajan nappulan ja tapporuudun välissä
CheckForKillAround tarkistaa kuoleeko joku kohderuudun ympärillä olevista nappuloista jos nappula siiretään kohderuutuun
"""