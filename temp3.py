import main

table = main.start()
print(table)
for row in table:
    row_txt = "|"
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