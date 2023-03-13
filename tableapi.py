from gameData import gameData
import math


def debug(message):
    if gameData["debug"]:
        print(message)


def getPosition():
    return gameData["currentPosition"]


def setPosition(fen):
    gameData["currentPosition"] = fen


def getKingMoved():
    return gameData["kingMoved"]


def kingMoved():
    gameData["kingMoved"] = True


def fen2list(fen):
    board = []
    rows = fen.split("/")
    for row in rows:
        for c in row:
            if c in "123456789":
                for i in range(int(c)):
                    board.append(None)
            elif c == "k":
                board.append(2)
            elif c == "a":
                board.append(1)
            elif c == "d":
                board.append(0)
    return board


def list2fen(board):
    fen = ""
    i = 0
    for c in board:
        if i % 9 == 0 and i != 0:
            fen = fen + "/"
        if c is None:
            if len(fen) > 0:
                if fen[-1] in "12345678":
                    fen = fen[:-1] + str(int(fen[-1]) + 1)
                else:
                    fen = fen + "1"
            elif len(fen) == 0:
                fen = fen + "1"
        elif c == 2:
            fen = fen + "k"
        elif c == 1:
            fen = fen + "a"
        elif c == 0:
            fen = fen + "d"
        i = i + 1
    return fen


def getIndex(square):
    squares = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
               "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
               "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
               "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
               "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9",
               "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
               "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
               "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9",
               "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"]
    return squares.index(square.upper())


def getSquare(index):
    squares = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
               "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
               "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
               "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
               "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9",
               "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
               "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
               "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9",
               "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"]
    return squares[index]


def movePiece(start_index, target_index):
    board = fen2list(getPosition())
    piece = board[start_index]
    board[start_index] = None
    board[target_index] = piece
    setPosition(list2fen(board))


def removePiece(index):
    board = fen2list(getPosition())
    board[index] = None
    setPosition(list2fen(board))


def getPiece(index):
    board = fen2list(getPosition())
    return board[index]


def getPieces():
    pieces = []
    board = fen2list(getPosition())
    i = 0
    for square in board:
        if square == 0 or square == 1 or square == 2:
            pieces.append(f"{i.zfill(3)}{square}")
        i = i + 1
    return pieces


def checkVertical(start_index, target_index):
    a = start_index + 1
    b = target_index + 1
    steps = int(abs((a - b) / 9))
    step = 9 * (b - a) / abs(b - a)
    for i in range(1, steps+1):
        if getPiece(int(start_index+(i*step))) is not None:
            return False
    return True


def checkHorizontal(start_index, target_index):
    a = start_index + 1
    b = target_index + 1
    steps = int(abs(a-b))
    step = (b - a) / abs(b - a)
    for i in range(1, steps+1):
        if getPiece(int(start_index+(i*step))) is not None:
            return False
    return True


def move(start_index, target_index):
    piece = getPiece(start_index)
    if isMoveLegal(start_index, target_index):
        movePiece(start_index, target_index)
        postMove(start_index, target_index, piece)
        printPosition(getPosition())
    return


def isMoveLegal(start_index, target_index):
    if 0 >= start_index >= 80 and 0 >= target_index >= 80:
        debug("Squares out of range!")
        return False
    if start_index == target_index:
        debug("Start square is same as target!")
        return False
    if getPiece(start_index) is None:
        debug("No piece selected!")
        return False
    if getPiece(target_index) is not None:
        debug("Target square is occupied!")
        return False
    if target_index == 40 or target_index == 0 or target_index == 8 or target_index == 72 or target_index == 80:
        if getPiece(start_index) != 2:
            debug("Target square is Throne or Corner and selected piece is not King!")
            return False
    if math.ceil((start_index+1)/9) == math.ceil((target_index+1)/9):
        if not checkHorizontal(start_index, target_index):
            debug("There is pieces on the way!(H)")
            return False
    elif abs(start_index-target_index) % 9 == 0:
        if not checkVertical(start_index, target_index):
            debug("There is pieces on the way!(V)")
            return False
    else:
        debug("Selected squares are not in a straight line")
        return False
    if checkForDeath(target_index, getPiece(start_index)):
        if not makesKill(start_index, target_index, getPiece(start_index)):
            debug("Target square would kill selected piece instantly")
            return False
    return True


def postMove(start_index, target_index, piece):
    if checkKingTrapped():
        printPosition(getPosition())
        defWin()
    if piece == 2:
        if start_index == 40:
            kingMoved()
            checkThroneKills()
        elif target_index == 0 or target_index == 8 or target_index == 72 or target_index == 80:
            printPosition(getPosition())
            atkWin()
    kill(target_index, piece)


def kill(target_index, piece):
    left, right, up, down = getKills(target_index, piece)
    if left:
        removePiece(target_index - 1)
    if right:
        removePiece(target_index + 1)
    if up:
        removePiece(target_index - 9)
    if down:
        removePiece(target_index + 9)


def checkForDeath(target_index, piece):
    left, right, up, down = checkForKillSquaresAround(target_index, piece)
    if piece != 2:
        if left and right:
            return True
        if up and down:
            return True
        return False
    return False


def checkForKillSquaresAround(target_index, piece):
    lo, ro, uo, do = oobCheck(target_index)
    left, right, up, down = False, False, False, False
    if not lo:
        if isEnemyOrKillSquare(target_index-1, piece):
            left = True
    if not ro:
        if isEnemyOrKillSquare(target_index+1, piece):
            right = True
    if not uo:
        if isEnemyOrKillSquare(target_index-9, piece):
            up = True
    if not do:
        if isEnemyOrKillSquare(target_index+9, piece):
            down = True

    return left, right, up, down


def oobCheck(target_index):
    left, right, up, down = False, False, False, False
    if target_index % 9 == 0:
        left = True
    if (target_index + 1) % 9 == 0:
        right = True
    if 0 <= target_index <= 8:
        up = True
    if 72 <= target_index <= 80:
        down = True

    return left, right, up, down


def isEnemyOrKillSquare(target_index, piece):
    if getPiece(target_index) == getEnemy(piece) or isKillSquare(target_index):
        return True
    return False


def getEnemy(piece):
    if piece == 1 or piece == 2:
        enemy = 0
    elif piece == 0:
        enemy = 1
    return enemy


def isKillSquare(target_index):
    if target_index == 0 or target_index == 8 or target_index == 72 or target_index == 80:
        return True
    elif target_index == 40:
        if getKingMoved():
            return True
    return False


def makesKill(start_index, target_index, piece):
    lo, ro, uo, do = oobCheck(target_index)
    movePiece(start_index, target_index)

    if not lo:
        if getPiece(target_index - 1) == getEnemy(piece):
            if checkForDeath(target_index - 1, getEnemy(piece)):
                movePiece(target_index, start_index)
                return True
    if not ro:
        if getPiece(target_index + 1) == getEnemy(piece):
            if checkForDeath(target_index + 1, getEnemy(piece)):
                movePiece(target_index, start_index)
                return True
    if not uo:
        if getPiece(target_index - 9) == getEnemy(piece):
            if checkForDeath(target_index - 9, getEnemy(piece)):
                movePiece(target_index, start_index)
                return True
    if not do:
        if getPiece(target_index + 9) == getEnemy(piece):
            if checkForDeath(target_index + 9, getEnemy(piece)):
                movePiece(target_index, start_index)
                return True

    movePiece(target_index, start_index)

    return False


def getKills(target_index, piece):
    left, right, up, down = False, False, False, False
    lo, ro, uo, do = oobCheck(target_index)

    if not lo:
        if getPiece(target_index - 1) == getEnemy(piece):
            if checkForDeath(target_index - 1, getEnemy(piece)):
                left = True
    if not ro:
        if getPiece(target_index + 1) == getEnemy(piece):
            if checkForDeath(target_index + 1, getEnemy(piece)):
                right = True
    if not uo:
        if getPiece(target_index - 9) == getEnemy(piece):
            if checkForDeath(target_index - 9, getEnemy(piece)):
                up = True
    if not do:
        if getPiece(target_index + 9) == getEnemy(piece):
            if checkForDeath(target_index + 9, getEnemy(piece)):
                down = True

    return left, right, up, down


def getKillsThrone():
    left, right, up, down = False, False, False, False
    if getPiece(39):
        if checkForDeath(39, getPiece(39)):
            left = True
    if getPiece(41):
        if checkForDeath(41, getPiece(41)):
            right = True
    if getPiece(31):
        if checkForDeath(31, getPiece(31)):
            up = True
    if getPiece(49):
        if checkForDeath(49, getPiece(49)):
            down = True
    return left, right, up, down


def checkKingTrapped():
    board = fen2list(getPosition())
    king_index = board.index(2)
    if king_index == 40:
        if not getKingMoved():
            return False
    left, right, up, down = oobCheck(king_index)
    if not left:
        if getPiece(king_index - 1) == 0:
            left = True
    if not right:
        if getPiece(king_index + 1) == 0:
            right = True
    if not up:
        if getPiece(king_index - 9) == 0:
            up = True
    if not down:
        if getPiece(king_index + 9) == 0:
            down = True
    if left and right and up and down:
        return True
    return False


def checkThroneKills():
    left, right, up, down = getKillsThrone()
    if left:
        removePiece(39)
    if right:
        removePiece(41)
    if up:
        removePiece(31)
    if down:
        removePiece(49)


def printPosition(fen):
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
    debug(board)


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


def defWin():
    debug("Defenders Win!")
    exit()


def atkWin():
    debug("Attackers Win!")
    exit()
