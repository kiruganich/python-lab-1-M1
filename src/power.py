import re
from .constants import (
    ERROR_INVALID_TOKEN,
    ERROR_DIVISION_BY_ZERO,
    ERROR_UNEXPECTED_END,
    ERROR_MISMATCHED_PARENTHESIS,
    ERROR_INVALID_NUMBER
)

def tokenize(expr: str) -> list:
    """Разбивает строку на токены: числа, операторы, скобки."""
    expr = expr.replace(' ', '')
    if not expr:
        raise ValueError(ERROR_INVALID_TOKEN)

    tokens = re.findall(r'\d+\.?\d*|\.\d+|\*\*|[+\-*/%()]', expr)

    if ''.join(tokens) != expr:
        raise ValueError(ERROR_INVALID_TOKEN)

    result = []
    for token in tokens:
        if token in ('**', '+', '-', '*', '/', '//', '%', '(', ')'):
            result.append(token)
        else:
            try:
                if '.' in token:
                    result.append(float(token))
                else:
                    result.append(int(token))
            except ValueError:
                raise ValueError(ERROR_INVALID_NUMBER)
    return result


def evaluate(expression: str) -> float:
    """Вычисляет арифметическое выражение со скобками и приоритетами."""
    tokens = tokenize(expression)
    pos = 0

    def peek():
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError(ERROR_UNEXPECTED_END)
        return tokens[pos]

    def consume():
        nonlocal pos
        token = peek()
        pos += 1
        return token

    def primary() -> float:
        nonlocal pos
        token = consume()
        if isinstance(token, (int, float)):
            return float(token)
        elif token == '(':
            result = expr()
            if pos >= len(tokens) or consume() != ')':
                raise ValueError(ERROR_MISMATCHED_PARENTHESIS)
            return result
        else:
            raise ValueError(ERROR_INVALID_TOKEN)

    def unary() -> float:
        nonlocal pos
        if pos < len(tokens) and peek() in ('+', '-'):
            op = consume()
            value = unary()
            return value if op == '+' else -value
        else:
            return primary()

    def pow_() -> float:
        left = unary()
        if pos < len(tokens) and peek() == '**':
            consume()
            right = pow_()
            return left ** right
        return left

    def mul() -> float:
        left = pow_()
        while pos < len(tokens) and peek() in ('*', '/', '//', '%'):
            op = consume()
            right = pow_()
            if op == '*':
                left *= right
            elif op == '/':
                if right == 0:
                    raise ValueError(ERROR_DIVISION_BY_ZERO)
                left /= right
            elif op == '//':
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("Оператор // допустим только для целых чисел")
                if right == 0:
                    raise ValueError(ERROR_DIVISION_BY_ZERO)
                left //= right
            elif op == '%':
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("Оператор % допустим только для целых чисел")
                if right == 0:
                    raise ValueError(ERROR_DIVISION_BY_ZERO)
                left %= right
        return left

    def add() -> float:
        left = mul()
        while pos < len(tokens) and peek() in ('+', '-'):
            op = consume()
            right = mul()
            if op == '+':
                left += right
            else:
                left -= right
        return left

    def expr() -> float:
        return add()

    result = expr()

    if pos != len(tokens):
        raise ValueError(ERROR_INVALID_TOKEN)

    return result