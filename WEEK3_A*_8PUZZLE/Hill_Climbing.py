import random

def print_board(state):
    for r in range(4):
        row_str = ""
        for c in range(4):
            if state[c] == r:
                row_str += "Q "
            else:
                row_str += ". "
        print(row_str)
    print()

def get_h_and_conflicts(state):
    attacks = 0
    conflicts = []
    for i in range(4):
        for j in range(i + 1, 4):
            # Check same row or same diagonal
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
                conflicts.append((i, j))
    return attacks, conflicts

def get_neighbors(state):
    neighbors = []
    for col in range(4):
        for row in range(4):
            if state[col] != row:
                neighbor = list(state)
                neighbor[col] = row
                neighbors.append(tuple(neighbor))
    return neighbors

def hill_climbing_queens(initial_state):
    current_state = initial_state
    current_h, current_conflicts = get_h_and_conflicts(current_state)
    path = [(current_state, current_h, current_conflicts)]
    
    while current_h > 0:
        neighbors = get_neighbors(current_state)
        best_neighbors = []
        best_h = current_h
        
        for neighbor in neighbors:
            h, _ = get_h_and_conflicts(neighbor)
            if h < best_h:
                best_h = h
                best_neighbors = [neighbor]
            elif h == best_h and h < current_h:
                best_neighbors.append(neighbor)
                
        if best_h >= current_h:
            break
            
        current_state = random.choice(best_neighbors)
        current_h, current_conflicts = get_h_and_conflicts(current_state)
        path.append((current_state, current_h, current_conflicts))
        
    return path, current_h == 0

def get_user_input():
    print("--- Enter Initial Positions for 4 Queens (Rows 0 to 3 for Columns 1 to 4) ---")
    while True:
        try:
            state = list(map(int, input("Enter 4 space-separated row placements: ").split()))
            if len(state) == 4 and all(0 <= r <= 3 for r in state):
                return tuple(state)
            print("Invalid input. Please enter exactly 4 numbers between 0 and 3.")
        except ValueError:
            print("Invalid input. Please enter integers only.")

initial = get_user_input()
path, success = hill_climbing_queens(initial)

for index, (state, h, conflicts) in enumerate(path):
    print(f"--- Stage {index} ---")
    print(f"Attacking pairs h(n) = {h}")
    print(f"State configuration: {state}")
    
    if conflicts:
        print("Conflicting Queens at columns:")
        for c1, c2 in conflicts:
            print(f"  - Queen at Col {c1} (Row {state[c1]}) conflicts with Queen at Col {c2} (Row {state[c2]})")
    else:
        print("No conflicts!")
        
    print_board(state)

if success:
    print("Success: Solved the 4-Queens problem!")
else:
    print("Failed: Stuck in a local minimum or plateau (cannot reduce attacks further).")
