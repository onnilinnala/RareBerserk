import main

table = main.start()
print(table)
def printCurrentTable():
    print("    |1|2|3|4|5|6|7|8|9")
    for row in table:
        row_txt = f"({row}) |"
        for column in range(9):
            if table[row][str(column + 1)]["Piece"] is None:
                row_txt = row_txt + ' |'
            elif table[row][str(column + 1)]["Piece"] == "1":
                row_txt = row_txt + 'D|'
            elif table[row][str(column + 1)]["Piece"] == "2":
                row_txt = row_txt + 'A|'
            elif table[row][str(column + 1)]["Piece"] == "3":
                row_txt = row_txt + 'K|'
            else:
                row_txt = row_txt + '!|'
        print(row_txt)

printCurrentTable()