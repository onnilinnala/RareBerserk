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
    table["A"]["9"]["KillSquare"] = True
    table["I"]["9"]["KillSquare"] = True
    table["A"]["1"]["KillSquare"] = True
    table["I"]["1"]["KillSquare"] = True
    tableapi.printCurrentTable()
    askForMove()


def askForMove():
    move_piece = input("Select piece: ").upper()
    target_square = input("Target square: ").upper()
    if not tableapi.checkSquareValidity(move_piece):
        print("Invalid square selected!\n")
        askForMove()
        return
    if not tableapi.checkSquareValidity(target_square):
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
