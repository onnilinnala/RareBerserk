def checkForKill(row, column, piece):
    left, right, up, down = checkForKillSquares(row, column, piece)
    if left and right:
        return True
    if up and down:
        return True
    return False


def checkForKillAround(row, column, piece):
    if piece == "1":
        piece = "2"
    elif piece == "2":
        piece = "1"
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
        left = checkForKill(row, str(int(column)-1), piece)
    if not right_oob:
        right = checkForKill(row, str(int(column)+1), piece)
    if not up_oob:
        up = checkForKill(intToLetter(letterToInt(row)-1), column, piece)
    if not down_oob:
        down = checkForKill(intToLetter(letterToInt(row)+1), column, piece)
    return left, right, up, down


def checkForKillSquares(row, column, target):
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