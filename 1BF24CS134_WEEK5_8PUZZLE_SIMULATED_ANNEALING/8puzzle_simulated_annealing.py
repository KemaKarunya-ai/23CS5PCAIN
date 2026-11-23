import random
import math

def calculate_cost(board):
    conflicts = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def simulated_annealing():
    while True:
        board = [random.randint(0, 7) for _ in range(8)]
        current_cost = calculate_cost(board)
        temperature = 10.0

        while temperature > 0.001 and current_cost != 0:
            col = random.randint(0, 7)
            new_row = random.randint(0, 7)

            while new_row == board[col]:
                new_row = random.randint(0, 7)

            new_board = board.copy()
            new_board[col] = new_row

            new_cost = calculate_cost(new_board)
            delta_E = new_cost - current_cost

            if delta_E < 0 or random.random() < math.exp(-delta_E / temperature):
                board = new_board
                current_cost = new_cost

            temperature *= 0.90

        if current_cost == 0:
            return board, current_cost

def print_board(board):
    for row in range(8):
        for col in range(8):
            print("Q" if board[col] == row else ".", end=" ")
        print()

solution, cost = simulated_annealing()

print("Final Board:", solution)
print("Final Cost:", cost)
print("Solution Found!")

print("\nChess Board:")
print_board(solution)
