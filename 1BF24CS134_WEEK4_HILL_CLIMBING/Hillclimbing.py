import random

def calculate_conflicts(state):
    """Calculates the number of attacking pairs of queens."""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(state):
    """Finds the best neighboring state by moving one queen within its column."""
    n = len(state)
    best_conflicts = calculate_conflicts(state)
    best_neighbors = []

    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue
            
            neighbor = list(state)
            neighbor[col] = row
            conflicts = calculate_conflicts(neighbor)

            if conflicts < best_conflicts:
                best_conflicts = conflicts
                best_neighbors = [neighbor]
            elif conflicts == best_conflicts:
                best_neighbors.append(neighbor)

    if best_neighbors:
        return random.choice(best_neighbors), best_conflicts
    return state, best_conflicts

def hill_climbing_from_input(initial_state, max_sideways=10):
    """Runs Steepest-Ascent Hill Climbing starting from a user-defined state."""
    current_state = list(initial_state)
    current_conflicts = calculate_conflicts(current_state)
    sideways_moves = 0
    steps = 0

    print(f"\nInitial State: {current_state} | Conflicts: {current_conflicts}")

    while current_conflicts > 0:
        next_state, next_conflicts = get_best_neighbor(current_state)
        steps += 1

        if next_conflicts < current_conflicts:
            current_state = next_state
            current_conflicts = next_conflicts
            sideways_moves = 0
            print(f"Step {steps}: {current_state} | Conflicts: {current_conflicts}")
        elif next_conflicts == current_conflicts and sideways_moves < max_sideways:
            current_state = next_state
            sideways_moves += 1
            print(f"Step {steps} (Sideways): {current_state} | Conflicts: {current_conflicts}")
        else:
            print("\nStopped: Stuck in a local optimum or plateau!")
            return current_state, False

    return current_state, True

def print_board(state):
    """Prints the 4x4 chessboard."""
    n = len(state)
    for row in range(n):
        line = ["Q" if state[col] == row else "." for col in range(n)]
        print(" ".join(line))

def get_user_input():
    """Prompts the user for 4 row indices (0 to 3)."""
    while True:
        try:
            raw = input("Enter 4 row positions (0-3) separated by spaces (e.g., 0 1 2 3): ")
            state = [int(x) for x in raw.strip().split()]
            
            if len(state) != 4 or any(r < 0 or r > 3 for r in state):
                print("Invalid input. Please enter exactly 4 numbers between 0 and 3.")
                continue
            return state
        except ValueError:
            print("Invalid input. Please enter integers only.")

# --- Main Execution ---
initial_board = get_user_input()
print("\nStarting Board:")
print_board(initial_board)

final_state, solved = hill_climbing_from_input(initial_board)

print("\nFinal Board:")
print_board(final_state)

if solved:
    print("\nSuccess: Valid 4-Queens solution reached!")
else:
    print("\nFailed: Standard Hill Climbing got stuck from this starting state.")
