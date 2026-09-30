from collections import deque

goal = (1,2,3,8,0,4,7,6,5)

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

def dfs(state, visited, path, best_path):
    
    if best_path[0] and len(path) >= len(best_path[0]):
        return

    if state == goal:
        if not best_path[0] or len(path) < len(best_path[0]):
            best_path[0] = list(path)
        return

    visited.add(state)

    
    for next_state in sorted(get_moves(state)):
        if next_state not in visited:
            dfs(next_state, visited, path + [next_state], best_path)

   
    visited.remove(state)


initial = (2,8,3,1,6,4,7,0,5)
visited = set()
container = [None] 
if not is_solvable(initial, goal):
    print("The puzzle is not solvable from the initial state to the specified goal state.")
else:
    print(f"Attempting DFS for initial {initial} to goal {goal}...")
    dfs(initial, visited, [initial], container)
    solution = container[0]

    if solution:
        print("DFS Solution found:")
        print("Number of moves:", len(solution) - 1)
        print()
        for state in solution:
            print_puzzle(state)
    else:
        print("No solution found by DFS within the recursion limit.")
