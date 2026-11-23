import re
import itertools

# ---------------------------------------------------------
# 1. PARSER & FORMATTER
# ---------------------------------------------------------

def parse_atom(text):
    """Parses 'Owns(CountryA, m1)' into ['Owns', 'CountryA', 'm1']."""
    text = text.strip()
    if "(" not in text:
        return [text]

    match = re.match(r"^([A-Za-z0-9_]+)\((.*)\)$", text)
    if not match:
        raise ValueError(f"Invalid predicate syntax: '{text}'")

    pred = match.group(1)
    args_str = match.group(2)

    args = []
    current = ""
    depth = 0
    for ch in args_str:
        if ch == "," and depth == 0:
            args.append(current.strip())
            current = ""
        else:
            current += ch
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
    if depth != 0:
        raise ValueError(f"Unbalanced parentheses in '{text}'")
    if current.strip():
        args.append(current.strip())

    return [pred] + [parse_atom(a)[0] if "(" not in a else parse_atom(a) for a in args]

def format_atom(atom):
    """Converts ['Owns', 'CountryA', 'm1'] back to 'Owns(CountryA, m1)'."""
    if isinstance(atom, str):
        return atom
    if len(atom) == 1:
        return atom[0]
    return f"{atom[0]}({', '.join(format_atom(a) for a in atom[1:])})"

def parse_rule(rule_str):
    """Parses 'P(x) ^ Q(x, y) -> R(y)' into (premises_list, conclusion)."""
    rule_str = rule_str.replace("=>", "->")
    if "->" not in rule_str:
        raise ValueError("Rule must contain '->' or '=>'.")

    lhs, rhs = rule_str.split("->", 1)
    raw_premises = re.split(r'\^|&|\bAND\b', lhs, flags=re.IGNORECASE)
    premises = [parse_atom(p) for p in raw_premises if p.strip()]
    conclusion = parse_atom(rhs)

    if not premises or not conclusion:
        raise ValueError("Missing premise or conclusion.")
    return premises, conclusion

# ---------------------------------------------------------
# 2. UNIFICATION ENGINE
# ---------------------------------------------------------

def is_variable(term):
    """Single lowercase letters (x, y, z, etc.) are treated as variables."""
    return isinstance(term, str) and len(term) == 1 and term.islower()

def apply_sub(sub, expr):
    if isinstance(expr, str):
        visited = set()
        while expr in sub and expr not in visited:
            visited.add(expr)
            expr = sub[expr]
        return expr
    if isinstance(expr, list):
        return [expr[0]] + [apply_sub(sub, a) for a in expr[1:]]
    return expr

def unify(x, y, sub=None):
    if sub is None:
        sub = {}
    else:
        sub = dict(sub)

    x = apply_sub(sub, x)
    y = apply_sub(sub, y)

    if x == y:
        return sub
    if is_variable(x):
        sub[x] = y
        return sub
    if is_variable(y):
        sub[y] = x
        return sub
    if isinstance(x, list) and isinstance(y, list):
        if x[0] != y[0] or len(x) != len(y):
            return None
        for a, b in zip(x[1:], y[1:]):
            sub = unify(a, b, sub)
            if sub is None:
                return None
        return sub
    return None

# ---------------------------------------------------------
# 3. FIRST-ORDER LOGIC FORWARD CHAINING
# ---------------------------------------------------------

def fol_forward_chaining(facts, rules, query):
    known_facts = list(facts)
    known_strs = {format_atom(f) for f in known_facts}
    query_str = format_atom(query)
    step = 1

    print("\n" + "=" * 65)
    print("FIRST-ORDER LOGIC FORWARD CHAINING TRACE")
    print("=" * 65)
    print("Initial Facts:", ", ".join(format_atom(f) for f in known_facts))
    print("Goal Query:   ", query_str, "\n")

    # Check if query already unifies with an initial fact
    for f in known_facts:
        if unify(f, query) is not None:
            print(f"Query '{query_str}' matches initial fact '{format_atom(f)}'!")
            return True

    while True:
        new_facts = []

        for premises, conclusion in rules:
            # Find candidate facts matching each premise predicate
            candidates_per_premise = []
            possible = True
            for p in premises:
                matches = [f for f in known_facts if f[0] == p[0] and len(f) == len(p)]
                if not matches:
                    possible = False
                    break
                candidates_per_premise.append(matches)

            if not possible:
                continue

            # Try all combinations of matching facts to unify all premises consistently
            for fact_combo in itertools.product(*candidates_per_premise):
                sub = {}
                for premise, fact in zip(premises, fact_combo):
                    sub = unify(premise, fact, sub)
                    if sub is None:
                        break

                if sub is not None:
                    inferred = apply_sub(sub, conclusion)
                    inferred_str = format_atom(inferred)

                    if inferred_str not in known_strs:
                        known_strs.add(inferred_str)
                        new_facts.append(inferred)

                        rule_display = " ^ ".join(format_atom(p) for p in premises) + " -> " + format_atom(conclusion)
                        sub_display = "{" + ", ".join(f"{k}/{format_atom(v)}" for k, v in sub.items()) + "}"
                        print(f"Step {step}: Fired [{rule_display}]")
                        print(f"        Substitution: {sub_display}")
                        print(f"        Inferred:     {inferred_str}\n")
                        step += 1

                        if unify(inferred, query) is not None:
                            return True

        if not new_facts:
            break
        known_facts.extend(new_facts)

    return False

# ---------------------------------------------------------
# 4. MAIN INPUT LOOP
# ---------------------------------------------------------

def get_valid_int(prompt):
    while True:
        try:
            val = int(input(prompt).strip())
            if val >= 0:
                return val
            print("Enter a non-negative integer.")
        except ValueError:
            print("Invalid input. Enter an integer.")

def main():
    print("=" * 65)
    print("       FIRST-ORDER LOGIC FORWARD CHAINING (FOL-FC)")
    print("=" * 65)
    print("Convention: Single lowercase letters (x, y, z) = Variables")
    print("            Words/Upper-case (m1, CountryA, West) = Constants\n")

    # 1. Number of Facts
    num_facts = get_valid_int("Enter number of facts: ")
    facts = []
    for i in range(num_facts):
        while True:
            try:
                raw = input(f"Enter Fact {i + 1}: ").strip()
                if not raw:
                    raise ValueError("Empty input")
                facts.append(parse_atom(raw))
                break
            except ValueError as e:
                print(f"Error: {e}. Try again.")

    # 2. Number of Rules
    num_rules = get_valid_int("\nEnter number of rules: ")
    print("Format: Premise1(x) ^ Premise2(x, y) -> Conclusion(y)")
    rules = []
    for i in range(num_rules):
        while True:
            try:
                raw = input(f"Enter Rule {i + 1}: ").strip()
                rules.append(parse_rule(raw))
                break
            except ValueError as e:
                print(f"Error: {e}. Try again.")

    # 3. Query
    while True:
        try:
            raw_q = input("\nEnter query to prove: ").strip()
            if not raw_q:
                raise ValueError("Empty query")
            query = parse_atom(raw_q)
            break
        except ValueError as e:
            print(f"Error: {e}. Try again.")

    # 4. Execute
    proved = fol_forward_chaining(facts, rules, query)

    print("=" * 65)
    if proved:
        print(f"RESULT: SUCCESS! Query '{format_atom(query)}' is PROVED.")
    else:
        print(f"RESULT: FAILURE! Query '{format_atom(query)}' CANNOT be proved.")
    print("=" * 65)

if __name__ == "__main__":
    main()
