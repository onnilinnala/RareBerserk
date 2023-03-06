normal_start = "x2ddd2x/4d4/4a4/d3a3d/ddaakaadd/d3a3d/4a4/4d4/x2ddd2x"


def printFenAsTable(fen):
    board = ""
    for row in fen.split('/'):
        b_row = "|"
        for c in row:
            if c == ' ':
                break
            elif c == "d":
                b_row = b_row + 'D|'
            elif c == "a":
                b_row = b_row + 'A|'
            elif c == "k":
                b_row = b_row + 'K|'
            elif c == "x":
                b_row = b_row + 'X|'
            elif c in '123456789':
                for i in range(int(c)):
                    b_row = b_row + ' |'
        board = board + b_row + "\n"
    print(board)

printFenAsTable(normal_start)