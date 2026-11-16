import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_player_move(board, player_name):
    while True:
        try:
            print(f"\n{player_name}'s turn.")
            i = int(input("Enter row index (0, 1, 2): "))
            j = int(input("Enter column index (0, 1, 2): "))
            if 0 <= i < 3 and 0 <= j < 3:
                if board[i][j] == ' ':
                    return i, j
                else:
                    print("That position is already taken! Try again.")
            else:
                print("Invalid input. Row and column indices must be 0, 1, or 2.")
        except ValueError:
            print("Please enter valid integers.")

def get_computer_move(board):
    print("\nComputer's turn...")
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(empty_cells)

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("1. Player 1 vs Player 2")
    print("2. Player vs Computer")
    
    while True:
        choice = input("Choose game mode (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
        
    board = [[' ' for _ in range(3)] for _ in range(3)]
    p1 = '*'
    p2 = 'o'
    
    print_board(board)
    
    current_player = p1
    player_name = "Player 1"
    
    while True:
        if choice == '2' and current_player == p2:
            i, j = get_computer_move(board)
        else:
            i, j = get_player_move(board, player_name)
            
        board[i][j] = current_player
        print_board(board)
        
        if check_win(board, current_player):
            print(f"{player_name} ({current_player}) won the game!")
            break
            
        if is_draw(board):
            print("It's a draw!")
            break
            
        if current_player == p1:
            current_player = p2
            player_name = "Player 2" if choice == '1' else "Computer"
        else:
            current_player = p1
            player_name = "Player 1"

if __name__ == "__main__":
    play_game()
