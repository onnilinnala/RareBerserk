from main_table import main_table as table


def changePiece(row, column, piece):
    table[row][column]["Piece"] = piece


def changeKill(row, column, kill):
    table[row][column]["KillSquare"] = kill


def getData(row, column, dataType):
    return table[row][column][dataType]


def move(piece, target_square):
    try:
        row = piece[0]
        column = piece[1]
        target_row = target_square[0]
        target_column = target_square[1]
        if row == "E" and column == "5":
            changeKill(row, column, True)
        piece = getData(row, column, "Piece")
        if target_row == "E" and target_column == "5":
            if piece != "3":
                print("Only king can enter the center square!")
                return
        elif target_row == "A" or target_row == "I":
            if target_column == "1" or target_column == "9":
                if piece != "3":
                    print("Only king can enter the corner!")
                    return
        if checkForKill(target_row, target_column, piece):
            print("Target square is instakill!")
            return
        is_valid_target = False
        if getData(target_row, target_column, "Piece") is None:
            is_valid_target = True
        else:
            pass
        if is_valid_target and piece:
            if column == target_column:
                if checkColumn(column, row, target_row):
                    success = True
                else:
                    success = False
            elif row == target_row:
                if checkRow(row, column, target_column):
                    success = True
                else:
                    success = False
            else:
                return
        else:
            return
        if success:
            changePiece(row, column, None)
            changePiece(target_row, target_column, piece)
            left, right, up, down = checkForKillAround(target_row, target_column, piece)
            print(left, right, up, down)
            if left:
                changePiece(target_row, str(int(target_column)-1), None)
            if right:
                changePiece(target_row, str(int(target_column)+1), None)
            if up:
                changePiece(intToLetter(letterToInt(target_row)-1), target_column, None)
            if down:
                changePiece(intToLetter(letterToInt(target_row)+1), target_column, None)
            printCurrentTable()
    except Exception as e:
        print(f"There was an exception: {e}")
        return


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


def checkForKillSquares(row, column, piece):
    if piece == "1":
        target = "2"
    elif piece == "2" or piece == "3":
        target = "1"
    left, right, up, down, left_oob, right_oob, up_oob, down_oob = False, False, False, False, False, False, False, False
    if letterToInt(row) == 1:
        up_oob = True
    if letterToInt(row) == 9:
        down_oob = True
    if column == "1":
        left_oob = True
    if column == "9":
        right_oob = True
    if not left_oob:
        if getData(row, str(int(column) - 1), "Piece") == target or getData(row, str(int(column) - 1), "KillSquare"):
            left = True
    if not right_oob:
        if getData(row, str(int(column)+1), "Piece") == target or getData(row, str(int(column)+1), "KillSquare"):
            right = True
    if not up_oob:
        if getData(intToLetter(letterToInt(row)-1), column, "Piece") == target or getData(intToLetter(letterToInt(row)-1), column, "KillSquare"):
            up = True
    if not down_oob:
        if getData(intToLetter(letterToInt(row)+1), column, "Piece") == target or getData(intToLetter(letterToInt(row)+1), column, "KillSquare"):
            down = True
    return left, right, up, down


def checkForKill(row, column, piece):
    left, right, up, down = checkForKillSquares(row, column, piece)
    if left and right:
        return True
    if up and down:
        return True
    return False


def checkForKillAround(row, column, piece):
    left, right, up, down, left_oob, right_oob, up_oob, down_oob = False, False, False, False, False, False, False, False
    if piece == "1":
        piece = "2"
    elif piece == "2":
        piece = "1"
    if letterToInt(row) == 1:
        up_oob = True
    if letterToInt(row) == 9:
        down_oob = True
    if column == "1":
        left_oob = True
    if column == "9":
        right_oob = True
    if not left_oob:
        left = checkForKill(row, str(int(column)-1), piece)
    if not right_oob:
        right = checkForKill(row, str(int(column)+1), piece)
    if not up_oob:
        up = checkForKill(intToLetter(letterToInt(row)-1), column, piece)
    if not down_oob:
        down = checkForKill(intToLetter(letterToInt(row)+1), column, piece)
    return left, right, up, down
