import ast
import math

pruned_branches = []


def max_value(node, alpha, beta, path_name="Root"):
  # TERMINAL-TEST(state): If node is an integer/float, it is a leaf
  if isinstance(node, (int, float)):
    return node, [f"{path_name}({node})"]

  v = -math.inf
  best_path = []

  for i, child in enumerate(node):
    child_name = f"{path_name}.{i+1}"
    val, path = min_value(child, alpha, beta, child_name)

    if val > v:
      v = val
      best_path = [path_name] + path

    # Beta cutoff: if v >= beta then return v 
    if v >= beta:
      for j in range(i + 1, len(node)):
        pruned_branches.append(f"{path_name}.{j+1} -> {node[j]}")
      return v, best_path

    alpha = max(alpha, v)

  return v, best_path


def min_value(node, alpha, beta, path_name="Root"):
  # TERMINAL-TEST(state): If node is an integer/float, it is a leaf
  if isinstance(node, (int, float)):
    return node, [f"{path_name}({node})"]

  v = math.inf
  best_path = []

  for i, child in enumerate(node):
    child_name = f"{path_name}.{i+1}"
    val, path = max_value(child, alpha, beta, child_name)

    if val < v:
      v = val
      best_path = [path_name] + path

    # Alpha cutoff: if v <= alpha then return v
    if v <= alpha:
      for j in range(i + 1, len(node)):
        pruned_branches.append(f"{path_name}.{j+1} -> {node[j]}")
      return v, best_path

    beta = min(beta, v)

  return v, best_path


# --- Main Execution ---
if __name__ == "__main__":
  print("Enter the game tree as nested lists (e.g., [[10, 9], [14, 18]]):")
  tree_input = input("Tree: ")
  game_tree = ast.literal_eval(tree_input)

  pruned_branches.clear()
  root_val, opt_path = max_value(game_tree, -math.inf, math.inf)

  print("\n--- Alpha-Beta Pruning Results ---")
  print(f"Value of Root Node (MAX): {root_val}")
  print(f"Optimal Path: {' -> '.join(opt_path)}")
  print(f"Pruned (Cutoff) Branches: {pruned_branches}")
