#Reza haji ghasemi
#session4 project

def initialize_board():
    return ["-" for _ in range(9)]

def display_board(board):
    print("\n  " + " | ".join(board[0:3]))
    print(" ---|---|---")
    print("  " + " | ".join(board[3:6]))
    print(" ---|---|---")
    print("  " + " | ".join(board[6:9]) + "\n")

def get_player_symbols():
    while True:
        player1 = input("player 1: chose X or O ").upper()
        if player1 in ("X", "O"):
            player2 = "O" if player1 == "X" else"X"
            return player1, player2
        print("only X or O is acceptable!")

def make_move(board, player):
    while True:
        try:
            position = int(input(f"game player; {player} (now choose: 1-9): "))
            if 1 <= position <= 9:
                idx = position - 1
                if board[idx] == "-":
                    board[idx] = player
                    return
                print("This index is not empty!")
            else:
                print("only numbers between 1-9 are allowed!")
        except ValueError:
            print("just enter a number not more!")

def check_winner(board):
    
    for i in range(0, 9, 3):
        if board[i] != "-" and board[i] == board[i+1] == board[i+2]:
            return board[i]
    
    for i in range(3):
        if board[i] != "-" and board[i] == board[i+3] == board[i+6]:
            return board[i]
    
    
    if board[0] != "-" and board[0] == board[4] == board[8]:
        return board[0]
    if board[2] != "-" and board[2] == board[4] == board[6]:
        return board[2]
    
    
    return "T" if "-" not in board else None

def switch_player(current):
    return "O" if current == "X" else "X"

def main():
    board = initialize_board()
    p1, p2 = get_player_symbols()
    current = p1
    winner = None
    
    print("\n game is started! ")
    
    while not winner:
        display_board(board)
        make_move(board, current)
        winner = check_winner(board)
        current = switch_player(current)
    
    display_board(board)
    
    if winner == "T":
        print(" Same!")
    else:
        print(f" **Player {winner} win the game!** ")


main()

