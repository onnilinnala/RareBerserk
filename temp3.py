import main
import tableapi

table = main.start()

def printCurrentTable():
    print("    |1|2|3|4|5|6|7|8|9|")
    for row in table:
        row_txt = f"({row}) |"
        for column in range(9):
            if table[row][str(column + 1)]["Piece"] is None:
                row_txt = row_txt + f' |'
            elif table[row][str(column + 1)]["Piece"] == "1":
                row_txt = row_txt + f'D|'
            elif table[row][str(column + 1)]["Piece"] == "2":
                row_txt = row_txt + f'A|'
            elif table[row][str(column + 1)]["Piece"] == "3":
                row_txt = row_txt + f'K|'
        print(row_txt)

move_piece = input("Select piece: ")
target_square = input("Target square: ")
printCurrentTable()
tableapi.move(move_piece, target_square)