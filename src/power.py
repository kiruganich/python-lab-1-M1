import re

from src import constants


def tokenize(expr: str):
    expr = expr.replace(" ", "")
    if not expr:
        raise ValueError(constants.ERROR_INVALID_TOKEN)

    tokens = re.findall(r"\d+\.?\d*|\.\d+|\*\*|//|[+\-*/%()]", expr)

    if "".join(tokens) != expr:
        raise ValueError(constants.ERROR_INVALID_TOKEN)

    result = []
    for token in tokens:
        if token in ("**", "+", "-", "*", "/", "//", "%", "(", ")"):
            result.append(token)
        else:
            try:
                if "." in token:
                    result.append(float(token))
                else:
                    result.append(int(token))
            except ValueError:
                raise ValueError(constants.ERROR_INVALID_NUMBER)
    return result


def evaluate(expression: str):
    tokens = tokenize(expression)
    pos = 0

    def peek():
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError(constants.ERROR_UNEXPECTED_END)
        return tokens[pos]

    def consume():
        nonlocal pos
        token = peek()
        pos += 1
        return token

    def primary():
        nonlocal pos
        token = consume()
        if isinstance(token, (int, float)):
            return token
        elif token == "(":
            result = expr()
            if pos >= len(tokens) or consume() != ")":
                raise ValueError(constants.ERROR_MISMATCHED_PARENTHESIS)
            return result
        else:
            raise ValueError(constants.ERROR_INVALID_TOKEN)

    def unary():
        nonlocal pos
        if pos < len(tokens) and peek() in ("+", "-"):
            op = consume()
            value = unary()
            return value if op == "+" else -value
        else:
            return primary()

    def pow_():
        left = unary()
        if pos < len(tokens) and peek() == "**":
            consume()
            right = pow_()
            if left == 0 and right == 0:
                raise ValueError(constants.ERROR_NOT_DEFINED)
            return left**right
        return left

    def mul():
        left = pow_()
        while pos < len(tokens) and peek() in ("*", "/", "//", "%"):
            op = consume()
            right = pow_()
            if op == "*":
                left *= right
            elif op == "/":
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left /= right
            elif op == "//":
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("// только для целых чисел")
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left //= right
            elif op == "%":
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("% только для целых чисел")
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left %= right
        return left

    def add():
        left = mul()
        while pos < len(tokens) and peek() in ("+", "-"):
            op = consume()
            right = mul()
            if op == "+":
                left += right
            else:
                left -= right
        return left

    def expr():
        return add()

    result = expr()

    if pos != len(tokens):
        raise ValueError(constants.ERROR_INVALID_TOKEN)

    return result
