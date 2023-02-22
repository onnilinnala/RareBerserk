from main_table import main_table as table
import tableapi


def start():
    # 0 = empty
    # 1 = defender (defends corners)
    # 2 = attacker (has king)
    # 3 = king
    table["A"]["4"]["Piece"] = "1"  # Defender
    table["A"]["5"]["Piece"] = "1"  # Defender
    table["A"]["6"]["Piece"] = "1"  # Defender
    table["B"]["5"]["Piece"] = "1"  # Defender
    table["C"]["5"]["Piece"] = "2"  # Attacker
    table["D"]["5"]["Piece"] = "2"  # Attacker
    table["D"]["1"]["Piece"] = "1"  # Defender
    table["D"]["9"]["Piece"] = "1"  # Defender
    table["E"]["1"]["Piece"] = "1"  # Defender
    table["E"]["2"]["Piece"] = "1"  # Defender
    table["E"]["3"]["Piece"] = "2"  # Attacker
    table["E"]["4"]["Piece"] = "2"  # Attacker
    table["E"]["5"]["Piece"] = "3"  # King
    table["E"]["6"]["Piece"] = "2"  # Attacker
    table["E"]["7"]["Piece"] = "2"  # Attacker
    table["E"]["8"]["Piece"] = "1"  # Defender
    table["E"]["9"]["Piece"] = "1"  # Defender
    table["F"]["1"]["Piece"] = "1"  # Defender
    table["F"]["5"]["Piece"] = "2"  # Attacker
    table["F"]["9"]["Piece"] = "1"  # Defender
    table["G"]["5"]["Piece"] = "2"  # Attacker
    table["H"]["5"]["Piece"] = "1"  # Defender
    table["I"]["4"]["Piece"] = "1"  # Defender
    table["I"]["5"]["Piece"] = "1"  # Defender
    table["I"]["6"]["Piece"] = "1"  # Defender
    print(table)
    askForMove()


def askForMove():
    move_piece = input("Select piece: ")
    # Check validity
    if len(move_piece) != 2:
        print("Invalid piece selected!\n")
        askForMove()
        return
    if move_piece[0] == "A" or move_piece[0] == "B" or move_piece[0] == "C" or move_piece[0] == "D" or move_piece[0] == "E" or move_piece[0] == "F" or move_piece[0] == "G" or move_piece[0] == "H" or move_piece[0] == "I":
        if move_piece[1] == "1" or move_piece[1] == "2" or move_piece[1] == "3" or move_piece[1] == "4" or move_piece[1] == "5" or move_piece[1] == "6" or move_piece[1] == "7" or move_piece[1] == "8" or move_piece[1] == "9":
            pass
        else:
            print("Invalid piece selected!\n")
            askForMove()
            return
    else:
        print("Invalid piece selected!\n")
        askForMove()


    target_square = input("Target square: ")
    # Check validity
    if len(target_square) != 2:
        print("Invalid piece selected!\n")
        askForMove()
        return
    if target_square[0] == "A" or target_square[0] == "B" or target_square[0] == "C" or target_square[0] == "D" or target_square[0] == "E" or target_square[0] == "F" or target_square[0] == "G" or target_square[0] == "H" or target_square[0] == "I":
        if target_square[1] == "1" or target_square[1] == "2" or target_square[1] == "3" or target_square[1] == "4" or target_square[1] == "5" or target_square[1] == "6" or target_square[1] == "7" or target_square[1] == "8" or target_square[1] == "9":
            pass
        else:
            print("Invalid piece selected!\n")
            askForMove()
            return
    else:
        print("Invalid square selected!\n")
        askForMove()
        return
    if target_square == move_piece:
        print("No move selected!\n")
        askForMove()
        return
    tableapi.move(move_piece, target_square)
    askForMove()
    return


start()
