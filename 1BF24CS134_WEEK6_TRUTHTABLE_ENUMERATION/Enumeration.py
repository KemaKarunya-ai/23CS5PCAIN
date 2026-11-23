from itertools import product
import re


# ---------------- OPERATORS ----------------

def implication(p, q):
    return (not p) or q


def biconditional(p, q):
    return p == q


# ---------------- TOKENIZER ----------------

def tokenize(expression):
    pattern = r'<->|->|[A-Za-z][A-Za-z0-9_]*|[()~&|]'
    return re.findall(pattern, expression.replace(" ", ""))


# ---------------- PARSER ----------------

class Parser:

    def __init__(self, tokens, model):
        self.tokens = tokens
        self.model = model
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token=None):
        current = self.current()

        if token is not None and current != token:
            raise ValueError(
                f"Expected '{token}' but found '{current}'"
            )

        self.position += 1
        return current

    # A <-> B
    def parse_biconditional(self):
        left = self.parse_implication()

        while self.current() == "<->":
            self.eat("<->")
            right = self.parse_implication()
            left = biconditional(left, right)

        return left

    # A -> B
    def parse_implication(self):
        left = self.parse_or()

        if self.current() == "->":
            self.eat("->")
            right = self.parse_implication()
            left = implication(left, right)

        return left

    # A | B
    def parse_or(self):
        left = self.parse_and()

        while self.current() == "|":
            self.eat("|")
            right = self.parse_and()
            left = left or right

        return left

    # A & B
    def parse_and(self):
        left = self.parse_not()

        while self.current() == "&":
            self.eat("&")
            right = self.parse_not()
            left = left and right

        return left

    # ~A
    def parse_not(self):
        if self.current() == "~":
            self.eat("~")
            return not self.parse_not()

        return self.parse_primary()

    # Variables / parentheses
    def parse_primary(self):

        token = self.current()

        if token == "(":
            self.eat("(")
            value = self.parse_biconditional()
            self.eat(")")
            return value

        if token is None:
            raise ValueError("Unexpected end of expression")

        if token in self.model:
            self.eat()
            return self.model[token]

        raise ValueError(f"Unknown symbol: {token}")


# ---------------- EVALUATE ----------------

def evaluate(expression, model):

    tokens = tokenize(expression)

    parser = Parser(tokens, model)

    result = parser.parse_biconditional()

    if parser.current() is not None:
        raise ValueError(
            f"Unexpected token: {parser.current()}"
        )

    return result


# ---------------- GET SYMBOLS ----------------

def get_symbols(expressions):

    symbols = set()

    for expression in expressions:

        tokens = tokenize(expression)

        for token in tokens:

            if re.fullmatch(
                r'[A-Za-z][A-Za-z0-9_]*',
                token
            ):
                symbols.add(token)

    return sorted(symbols)


# ---------------- BUILD KB ----------------

def build_kb(statements):

    return " & ".join(
        f"({statement})"
        for statement in statements
    )


# ---------------- PRINT TRUTH TABLE ----------------

def print_truth_table(
    symbols,
    rows,
    statements,
    queries
):

    print("\n")
    print("=" * 150)
    print("TRUTH TABLE")
    print("=" * 150)

    headers = []

    # Propositional symbols
    headers.extend(symbols)

    # Individual KB statements
    for i, statement in enumerate(statements, 1):
        headers.append(
            f"S{i}({statement})"
        )

    # Complete KB
    headers.append("KB")

    # Queries
    headers.extend(queries)

    # Header
    print(
        " | ".join(
            f"{header:^15}"
            for header in headers
        )
    )

    print("-" * 150)

    # Rows
    for row in rows:

        values = []

        # Symbols
        for symbol in symbols:
            values.append(
                "T" if row[symbol] else "F"
            )

        # Individual statements
        for i in range(1, len(statements) + 1):

            values.append(
                "T" if row[f"S{i}"] else "F"
            )

        # KB
        values.append(
            "T" if row["KB"] else "F"
        )

        # Queries
        for i in range(1, len(queries) + 1):

            values.append(
                "T" if row[f"Q{i}"] else "F"
            )

        print(
            " | ".join(
                f"{value:^15}"
                for value in values
            )
        )

    print("=" * 150)


# ---------------- MAIN ----------------

def main():

    print("=" * 90)
    print("PROPOSITIONAL LOGIC - TRUTH TABLE ENUMERATION")
    print("=" * 90)

    print("\nOperators:")
    print("~   = NOT")
    print("&   = AND")
    print("|   = OR")
    print("->  = IMPLICATION")
    print("<-> = BICONDITIONAL")

    # ---------------- KB ----------------

    print("\n")
    print("=" * 90)
    print("ENTER KNOWLEDGE BASE")
    print("=" * 90)

    print("Enter KB statements one by one.")
    print("Enter 0 when finished.\n")

    statements = []

    while True:

        statement = input(
            f"Enter KB statement {len(statements) + 1}: "
        ).strip()

        if statement == "0":
            break

        if statement == "":
            print("Please enter a valid statement.")
            continue

        statements.append(statement)

    if not statements:

        print("\nError: Knowledge Base cannot be empty.")
        return

    kb = build_kb(statements)

    print("\n")
    print("=" * 90)
    print("KNOWLEDGE BASE")
    print("=" * 90)

    for i, statement in enumerate(statements, 1):
        print(f"S{i}: {statement}")

    print("\nCombined KB:")
    print(kb)

    # ---------------- QUERIES ----------------

    print("\n")
    print("=" * 90)
    print("ENTER QUERIES")
    print("=" * 90)

    print("Enter queries one by one.")
    print("Enter 0 when finished.\n")

    queries = []

    while True:

        query = input(
            f"Enter query {len(queries) + 1}: "
        ).strip()

        if query == "0":
            break

        if query == "":
            print("Please enter a valid query.")
            continue

        queries.append(query)

    if not queries:

        print("\nNo queries entered.")
        return

    # ---------------- SYMBOLS ----------------

    all_expressions = statements + queries

    symbols = get_symbols(all_expressions)

    # ---------------- TRUTH TABLE ----------------

    rows = []

    for values in product(
        [False, True],
        repeat=len(symbols)
    ):

        # Current model
        model = dict(
            zip(symbols, values)
        )

        # IMPORTANT:
        # Start row with the propositional symbols
        row = model.copy()

        # Evaluate EVERY individual KB statement
        for i, statement in enumerate(
            statements,
            start=1
        ):

            row[f"S{i}"] = evaluate(
                statement,
                model
            )

        # Evaluate complete KB
        row["KB"] = all(
            row[f"S{i}"]
            for i in range(
                1,
                len(statements) + 1
            )
        )

        # Evaluate queries
        for i, query in enumerate(
            queries,
            start=1
        ):

            row[f"Q{i}"] = evaluate(
                query,
                model
            )

        rows.append(row)

    # ---------------- PRINT TABLE ----------------

    print_truth_table(
        symbols,
        rows,
        statements,
        queries
    )

    # ---------------- ENTAILMENT ----------------

    print("\n")
    print("=" * 90)
    print("ENTAILMENT RESULTS")
    print("=" * 90)

    for i, query in enumerate(
        queries,
        start=1
    ):

        entails = True

        for row in rows:

            # Only consider models where KB is TRUE
            if row["KB"]:

                # If query is FALSE, KB does not entail it
                if not row[f"Q{i}"]:

                    entails = False
                    break

        print(f"\nQuery {i}: {query}")

        if entails:

            print("Result: YES")
            print(
                f"Therefore: KB |= {query}"
            )

        else:

            print("Result: NO")
            print(
                f"Therefore: KB !|= {query}"
            )


# ---------------- RUN ----------------

if __name__ == "__main__":
    main()
