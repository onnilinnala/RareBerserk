from main_table import main_table as table


def changePiece(row, column, piece):
    table[row][column]["Piece"] = piece


def changeKill(row, column, kill):
    table[row][column]["KillSquare"] = kill


def getData(row, column, dataType):
    return table[row][column][dataType]


def move(piece, target_square):
    row = piece[0]
    column = piece[1]
    target_row = target_square[0]
    target_column = target_square[1]
    piece = None
    is_valid_square = False
    if table[row][column]["Piece"] is None:
        pass
    elif table[row][column]["Piece"] == "1":
        piece = "Defender"
    elif table[row][column]["Piece"] == "2":
        piece = "Attacker"
    elif table[row][column]["Piece"] == "3":
        piece = "King"
    if table[target_row][target_column]["Piece"] is None:
        is_valid_square = True
    else:
        pass
    if is_valid_square and piece:
        if column == target_column:
            if
        elif row == target_row:


