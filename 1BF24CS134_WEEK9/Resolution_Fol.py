import copy


def is_variable(term):
  # Variables start with a lowercase letter (e.g., x, y)
  # Constants start with an uppercase letter (e.g., John, Apple)
  return isinstance(term, str) and len(term) > 0 and term[0].islower()


def unify(x, y, subs=None):
  if subs is None:
    subs = {}
  if subs is None:
    return None
  elif x == y:
    return subs
  elif is_variable(x):
    return unify_var(x, y, subs)
  elif is_variable(y):
    return unify_var(y, x, subs)
  elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
    s = unify(x[0], y[0], subs)
    return unify(x[1:], y[1:], s) if s is not None else None
  else:
    return None


def unify_var(var, x, subs):
  if var in subs:
    return unify(subs[var], x, subs)
  elif is_variable(x) and x in subs:
    return unify(var, subs[x], subs)
  else:
    new_subs = subs.copy()
    new_subs[var] = x
    return new_subs


def apply_subs(literal, subs):
  neg, pred, args = literal
  new_args = []
  for arg in args:
    while arg in subs:
      arg = subs[arg]
    new_args.append(arg)
  return (neg, pred, new_args)


def parse_literal(lit_str):
  lit_str = lit_str.strip()
  neg = False
  if lit_str.startswith('~'):
    neg = True
    lit_str = lit_str[1:].strip()

  pred, args_str = lit_str.split('(')
  args = [a.strip() for a in args_str[:-1].split(',')]
  return (neg, pred.strip(), args)


def parse_clause(clause_str):
  # Splits disjunctions separated by '|'
  return [parse_literal(lit) for lit in clause_str.split('|')]


def format_clause(clause):
  if not clause:
    return '[] (Empty Clause - Contradiction!)'
  parts = []
  for neg, pred, args in clause:
    prefix = '~' if neg else ''
    parts.append(f"{prefix}{pred}({', '.join(args)})")
  return ' | '.join(parts)


def format_subs(subs):
  if not subs:
    return '{}'
  return '{' + ', '.join(f'{k}/{v}' for k, v in subs.items()) + '}'


def resolve(ci, cj):
  resolvents = []
  for i, lit_i in enumerate(ci):
    for j, lit_j in enumerate(cj):
      # Check if predicates match and signs are opposite
      if lit_i[1] == lit_j[1] and lit_i[0] != lit_j[0]:
        subs = unify(lit_i[2], lit_j[2])
        if subs is not None:
          new_ci = [apply_subs(l, subs) for k, l in enumerate(ci) if k != i]
          new_cj = [apply_subs(l, subs) for k, l in enumerate(cj) if k != j]
          # Remove duplicates while preserving order
          resolvent = []
          for l in new_ci + new_cj:
            if l not in resolvent:
              resolvent.append(l)
          resolvents.append((resolvent, subs))
  return resolvents


def print_resolution_tree(nodes, goal_idx, prefix='', is_last=True):
  """Recursively prints the ASCII resolution proof tree from the root node."""
  node = nodes[goal_idx]
  connector = '└── ' if is_last else '├── '
  sub_info = f"  [Subs: {format_subs(node['subs'])}]" if node['subs'] else ''

  if node['parents'] is None:
    print(
        f'{prefix}{connector}[Clause {goal_idx + 1}]'
        f" {format_clause(node['clause'])}"
    )
  else:
    print(
        f"{prefix}{connector}{format_clause(node['clause'])}{sub_info}"
    )
    child_prefix = prefix + ('    ' if is_last else '│   ')
    p1, p2 = node['parents']
    print_resolution_tree(nodes, p1, child_prefix, is_last=False)
    print_resolution_tree(nodes, p2, child_prefix, is_last=True)


def fol_resolution(kb_clauses, query_str):
  clauses = copy.deepcopy(kb_clauses)

  # Negate the query and add to clauses
  q_neg, q_pred, q_args = parse_literal(query_str)
  negated_query = [(not q_neg, q_pred, q_args)]
  clauses.append(negated_query)

  # Track tree nodes: each entry stores clause, parent indices, and substitution used
  nodes = [{'clause': c, 'parents': None, 'subs': None} for c in clauses]

  print('\n--- Initial Clauses (KB + Negated Query) ---')
  for idx, c in enumerate(clauses, 1):
    print(f'{idx}. {format_clause(c)}')

  print('\n--- Resolution Steps ---')
  while True:
    n = len(clauses)
    new_entries = []

    for i in range(n):
      for j in range(i + 1, n):
        resolvents = resolve(clauses[i], clauses[j])
        for res, subs in resolvents:
          print(
              f'Resolved ({format_clause(clauses[i])}) & '
              f'({format_clause(clauses[j])})  ==>  {format_clause(res)}'
          )
          if not res:  # Empty clause found
            nodes.append({'clause': res, 'parents': (i, j), 'subs': subs})
            print('\n--- Resolution Proof Tree ---')
            print_resolution_tree(nodes, len(nodes) - 1)
            return True

          # Check if resolvent is already known
          existing = [entry['clause'] for entry in new_entries]
          if res not in clauses and res not in existing:
            new_entries.append({'clause': res, 'parents': (i, j), 'subs': subs})

    if not new_entries:
      return False

    for entry in new_entries:
      clauses.append(entry['clause'])
      nodes.append(entry)


# --- User Input Section ---
if __name__ == '__main__':
  print('=== First-Order Logic (FOL) Resolution Prover ===')
  print(
      'Syntax Guide: Use ~ for NOT, | for OR, lowercase for variables (x, y),'
      ' Uppercase for constants (John, Food).'
  )

  num_clauses = int(input('\nEnter number of CNF clauses in Knowledge Base: '))
  kb = []
  for i in range(num_clauses):
    c_str = input(f'Enter Clause {i+1}: ')
    kb.append(parse_clause(c_str))

  query = input('\nEnter the Goal Query to prove (single literal): ')

  result = fol_resolution(kb, query)
  print('\n--- Final Result ---')
  if result:
    print(f'SUCCESS: The query "{query}" is PROVED TRUE by refutation!')
  else:
    print(f'FAILURE: The query "{query}" CANNOT be proved from the KB.')
