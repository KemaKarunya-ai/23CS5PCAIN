import random
import math


# Calculate number of conflicts
def calculate_cost(board):
    conflicts = 0

    for c1 in range(8):
        for c2 in range(c1 + 1, 8):

            r1 = board[c1]
            r2 = board[c2]

            # Same row
            if r1 == r2:
                conflicts += 1

            # Same diagonal
            elif abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1

    return conflicts


# Generate a random neighbour
def get_neighbor(board):
    next_board = board.copy()

    # Pick random column
    col = random.randint(0, 7)

    # Pick a different random row
    new_row = random.randint(0, 7)

    while new_row == next_board[col]:
        new_row = random.randint(0, 7)

    next_board[col] = new_row

    return next_board


# Display chess board
def print_board(board):
    for row in range(8):
        for col in range(8):

            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        print()


# ------------------------------------------------
# SIMULATED ANNEALING
# ------------------------------------------------

def simulated_annealing():

    # 1. current ← initial state
    current = [0, 1, 2, 3, 4, 5, 6, 7]

    # 2. T ← a large positive value
    T = 10.0

    # Cooling factor
    alpha = 0.90

    iteration = 0

    print("Initial State:")
    print(current)
    print("Initial Cost:", calculate_cost(current))
    print()

    # 3. while T > 0
    while T > 0.001:

        # If solution is found
        if calculate_cost(current) == 0:
            break

        # 4. next ← random neighbour of current
        next_state = get_neighbor(current)

        current_cost = calculate_cost(current)
        next_cost = calculate_cost(next_state)

        # 5. ΔE ← current.cost - next.cost
        delta_E = current_cost - next_cost

        # 6. if ΔE > 0
        if delta_E > 0:

            # 7. current ← next
            current = next_state

            decision = "ACCEPTED - Better State"
            probability = 1.0
            random_value = 0.0

        else:

            # 9. p = e^(ΔE / T)
            probability = math.exp(delta_E / T)

            random_value = random.random()

            # Accept with probability p
            if random_value < probability:

                current = next_state
                decision = "ACCEPTED - Probability"

            else:

                decision = "REJECTED"

        # Display information
        print("----------------------------------------")
        print("Iteration:", iteration)
        print("Current Cost:", current_cost)
        print("Next Cost:", next_cost)
        print("Delta E:", delta_E)
        print("Temperature:", round(T, 4))
        print("Probability:", round(probability, 4))
        print("Random Value:", round(random_value, 4))
        print("Decision:", decision)
        print("Current State:", current)

        # 11. decrease T
        T = T * alpha

        iteration += 1

    # 13. return current
    print("\n========================================")
    print("FINAL RESULT")
    print("========================================")

    print("Final State:", current)
    print("Final Cost:", calculate_cost(current))
    print("Iterations:", iteration)

    print("\nChess Board:")
    print_board(current)

    if calculate_cost(current) == 0:
        print("\nSolution Found!")
    else:
        print("\nSolution Not Found.")

    return current


# Run the algorithm
simulated_annealing()
