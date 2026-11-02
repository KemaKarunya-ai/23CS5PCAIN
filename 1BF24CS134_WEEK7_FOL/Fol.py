import re


# ---------------------------------------------------------
# PARSE EXPRESSION
# ---------------------------------------------------------

def parse_expression(text):
    text = text.replace(" ", "")

    if not text:
        return ""

    # Simple variable or constant
    if "(" not in text:
        return text

    match = re.match(r"^([A-Za-z0-9_]+)\((.*)\)$", text)

    if not match:
        raise ValueError("Invalid expression: " + text)

    name = match.group(1)
    args_string = match.group(2)

    args = []
    current = ""
    depth = 0

    for char in args_string:

        if char == "," and depth == 0:
            args.append(current)
            current = ""

        else:
            current += char

            if char == "(":
                depth += 1

            elif char == ")":
                depth -= 1

    if current:
        args.append(current)

    return [name] + [parse_expression(arg) for arg in args]


# ---------------------------------------------------------
# FORMAT EXPRESSION
# ---------------------------------------------------------

def format_expression(expr):

    if isinstance(expr, str):
        return expr

    if isinstance(expr, list):
        name = expr[0]

        if len(expr) == 1:
            return name

        return name + "(" + ", ".join(
            format_expression(arg) for arg in expr[1:]
        ) + ")"

    return str(expr)


# ---------------------------------------------------------
# CHECK VARIABLE
# ---------------------------------------------------------

def is_variable(term):
    """
    Variables:
        x, y, z
        X, Y, Z
    """

    if not isinstance(term, str):
        return False

    # Uppercase single-letter variables
    if len(term) == 1 and term.isupper():
        return True

    # Lowercase single-letter variables
    if len(term) == 1 and term.islower():
        return True

    return False


# ---------------------------------------------------------
# OCCURS CHECK
# ---------------------------------------------------------

def occurs(variable, expression):

    # variable == expression
    if variable == expression:
        return True

    # Compound expression
    if isinstance(expression, list):

        for argument in expression[1:]:

            if occurs(variable, argument):
                return True

    return False


# ---------------------------------------------------------
# APPLY SUBSTITUTION
# ---------------------------------------------------------

def apply_substitution(substitution, expression):

    if isinstance(expression, str):

        # Keep replacing until final value is reached
        visited = set()

        while expression in substitution:

            if expression in visited:
                break

            visited.add(expression)

            expression = substitution[expression]

        return expression

    if isinstance(expression, list):

        return [
            expression[0]
        ] + [
            apply_substitution(substitution, arg)
            for arg in expression[1:]
        ]

    return expression


# ---------------------------------------------------------
# UNIFICATION ALGORITHM
# ---------------------------------------------------------

def unify(x, y, substitution=None):

    if substitution is None:
        substitution = {}

    # Apply current substitutions
    x = apply_substitution(substitution, x)
    y = apply_substitution(substitution, y)

    # -----------------------------------------------------
    # CASE 1: Same expressions
    # -----------------------------------------------------

    if x == y:
        return substitution

    # -----------------------------------------------------
    # CASE 2: x is a variable
    # -----------------------------------------------------

    if is_variable(x):

        # Occurs check
        if occurs(x, y):

            print(
                "FAILURE: Occurs check failed:",
                x,
                "occurs in",
                format_expression(y)
            )

            return None

        print(
            "Substitute:",
            x,
            "->",
            format_expression(y)
        )

        substitution[x] = y

        return substitution

    # -----------------------------------------------------
    # CASE 3: y is a variable
    # -----------------------------------------------------

    if is_variable(y):

        if occurs(y, x):

            print(
                "FAILURE: Occurs check failed:",
                y,
                "occurs in",
                format_expression(x)
            )

            return None

        print(
            "Substitute:",
            y,
            "->",
            format_expression(x)
        )

        substitution[y] = x

        return substitution

    # -----------------------------------------------------
    # CASE 4: Both are compound expressions
    # -----------------------------------------------------

    if isinstance(x, list) and isinstance(y, list):

        # Function/predicate names must match
        if x[0] != y[0]:

            print(
                "FAILURE: Function mismatch:",
                x[0],
                "!=",
                y[0]
            )

            return None

        # Number of arguments must match
        if len(x) != len(y):

            print(
                "FAILURE: Arity mismatch in",
                x[0]
            )

            return None

        # Unify every argument
        for i in range(1, len(x)):

            print(
                "Matching:",
                format_expression(
                    apply_substitution(substitution, x[i])
                ),
                "with",
                format_expression(
                    apply_substitution(substitution, y[i])
                )
            )

            substitution = unify(
                x[i],
                y[i],
                substitution
            )

            if substitution is None:
                return None

        return substitution

    # -----------------------------------------------------
    # CASE 5: Constants don't match
    # -----------------------------------------------------

    print(
        "FAILURE: Cannot unify",
        format_expression(x),
        "with",
        format_expression(y)
    )

    return None


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("        FIRST ORDER LOGIC UNIFICATION")
    print("=" * 60)

    expression1 = input("Enter Expression 1: ")
    expression2 = input("Enter Expression 2: ")

    try:

        # Parse expressions
        expr1 = parse_expression(expression1)
        expr2 = parse_expression(expression2)

        print("\nParsed Expression 1:")
        print(format_expression(expr1))

        print("\nParsed Expression 2:")
        print(format_expression(expr2))

        print("\n" + "-" * 60)
        print("UNIFICATION TRACE")
        print("-" * 60)

        # Perform unification
        result = unify(expr1, expr2)

        print("\n" + "=" * 60)

        if result is None:

            print("Result: UNIFICATION FAILED")

        else:

            print("Result: UNIFICATION SUCCESSFUL")

            if len(result) == 0:

                print("MGU: {}")

            else:

                print("MGU:")

                for variable, value in result.items():

                    value = apply_substitution(result, value)

                    print(
                        "   ",
                        variable,
                        "->",
                        format_expression(value)
                    )

        print("=" * 60)

    except Exception as e:

        print("Error:", e)


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
