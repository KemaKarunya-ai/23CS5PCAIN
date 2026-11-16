import heapq

def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])
    print()

def get_moves(state):
    moves = []
    zero = state.index(0)
    row = zero // 3
    col = zero % 3
    if row > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 3] = new_state[zero - 3], new_state[zero]
        moves.append(tuple(new_state))
    if row < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 3] = new_state[zero + 3], new_state[zero]
        moves.append(tuple(new_state))
    if col > 0:
        new_state = list(state)
        new_state[zero], new_state[zero - 1] = new_state[zero - 1], new_state[zero]
        moves.append(tuple(new_state))
    if col < 2:
        new_state = list(state)
        new_state[zero], new_state[zero + 1] = new_state[zero + 1], new_state[zero]
        moves.append(tuple(new_state))
    return moves

def get_inversions(state):
    inversions = 0
    arr = [i for i in state if i != 0]
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def is_solvable(initial_state, goal_state):
    initial_inversions = get_inversions(initial_state)
    goal_inversions = get_inversions(goal_state)
    return (initial_inversions % 2) == (goal_inversions % 2)

def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(9):
        tile = state[i]
        if tile != 0:
            goal_index = goal_state.index(tile)
            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def a_star_search(initial_state, goal_state):
    h_initial = manhattan_distance(initial_state, goal_state)
    open_set = [(h_initial, 0, initial_state, [(initial_state, 0, h_initial)])]
    g_score = {initial_state: 0}
    
    while open_set:
        f, g, state, path = heapq.heappop(open_set)
        
        if state == goal_state:
            return path
            
        if g > g_score.get(state, float('inf')):
            continue
            
        for next_state in get_moves(state):
            tentative_g = g + 1
            if tentative_g < g_score.get(next_state, float('inf')):
                g_score[next_state] = tentative_g
                h = manhattan_distance(next_state, goal_state)
                f_cost = tentative_g + h
                heapq.heappush(open_set, (f_cost, tentative_g, next_state, path + [(next_state, tentative_g, h)]))
                
    return None

def parse_state_input(prompt):
    print(prompt)
    state = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Enter row {i + 1} (3 space-separated numbers): ").split()))
                if len(row) == 3:
                    state.extend(row)
                    break
                print("Invalid input. Please enter exactly 3 numbers.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
    return tuple(state)

initial = parse_state_input("--- Enter Initial State (use 0 for empty space) ---")
goal = parse_state_input("--- Enter Goal State (use 0 for empty space) ---")

if len(set(initial)) != 9 or max(initial) > 8 or min(initial) < 0 or len(set(goal)) != 9 or max(goal) > 8 or min(goal) < 0:
    print("\nError: Both states must contain unique numbers from 0 to 8.")
elif not is_solvable(initial, goal):
    print("\nThe puzzle is not solvable from the initial state to the specified goal state.")
else:
    print(f"\nAttempting A* Search for initial {initial} to goal {goal}...\n")
    solution = a_star_search(initial, goal)
    
    if solution:
        print("A* Solution found:")
        print("Number of moves:", len(solution) - 1)
        print()
        for index, (state, g, h) in enumerate(solution):
            print(f"--- Stage {index} ---")
            print(f"g(n) = {g}, h(n) = {h}, f(n) = {g + h}")
            print_puzzle(state)
    else:
        print("No solution found.")
