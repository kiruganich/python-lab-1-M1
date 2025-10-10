import re
from typing import List, Union
from src import constants

Token = Union[float, str]

def tokenize(expr: str) -> List[Token]:
    expr = expr.replace(' ', '')
    if not expr:
        raise ValueError(constants.ERROR_INVALID_TOKEN)

    token_pattern = r'(\d+\.?\d*|\.\d+|[+\-*/%()]|\*\*)'
    tokens = re.findall(token_pattern, expr)
 
    if not tokens or ''.join(tokens) != expr:
        raise ValueError(constants.ERROR_INVALID_TOKEN)

    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in '+-' and (i == 0 or tokens[i - 1] in '(+-*/%'):
            if i + 1 >= len(tokens):
                raise ValueError(constants.ERROR_UNEXPECTED_END)
            next_token = tokens[i + 1]
            if next_token == '(':
                result.append(token)
                i += 1
            else:
                try: 
                    num = float(next_token)
                    if token == '-':
                        num = -num
                    result.append(num)
                    i += 2
                except ValueError:
                    raise ValueError(constants.ERROR_INVALID_NUMBER)
        elif token == '**':
            result.append('**')
            i += 1
        elif token in '()':
            result.append(token)
            i += 1
        elif token in '+-*/%':
            result.append(token)
            i += 1
        else:
            try:
                if '.' in token:
                    result.append(float(token))
                else:
                    result.append(int(token))
                i += 1
            except ValueError:
                raise ValueError(constants.ERROR_INVALID_NUMBER)
    return result

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos >= len(self.tokens):
            raise ValueError(constants.ERROR_UNEXPECTED_END)
        return self.tokens[self.pos]

    def consume(self) -> Token:
        token = self.peek()
        self.pos += 1
        return token

    def parse(self) -> float:
        result = self.expr()
        if self.pos != len(self.tokens):
            raise ValueError(constants.ERROR_INVALID_TOKEN)
        return result

    def expr(self) -> float:
        return self.add()

    def add(self) -> float:
        left = self.mul()
        while self.pos < len(self.tokens) and self.peek() in ('+', '-'):
            op = self.consume()
            right = self.mul()
            if op == '+':
                left += right
            else:
                left -= right
        return left

    def mul(self) -> float:
        left = self.pow()
        while self.pos < len(self.tokens) and self.peek() in ('*', '/', '//', '%'):
            op = self.consume()
            right = self.pow()
            if op == '*':
                left *= right
            elif op == '/':
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left /= right
            elif op == '//':
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("Деление без остатка допустимо только для целых чисел")
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left //= right
            elif op == '%':
                if not (isinstance(left, int) and isinstance(right, int)):
                    raise ValueError("Нахождение остатка допустимо только для целых чисел")
                if right == 0:
                    raise ValueError(constants.ERROR_DIVISION_BY_ZERO)
                left %= right
        return left

    def pow(self) -> float:
        left = self.unary()
        if self.pos < len(self.tokens) and self.peek() == '**':
            self.consume()
            right = self.pow() #Возведение в степеь - правоассоциативная операция
            return left ** right
        return left

    def unary(self) -> float:
        if self.pos < len(self.tokens) and self.peek() in ('+', '-'):
            op = self.consume()
            value = self.unary()
            return value if op == '+' else -value
        else:
            return self.primary()

    def primary(self) -> float:
        token = self.consume()
        if isinstance(token, (int, float)):
            return float(token)
        elif token == '(':
            result = self.expr()
            if self.pos >= len(self.tokens) or self.consume() != ')':
                raise ValueError(constants.ERROR_MISMATCHED_PARENTHESIS)
            return result
        else:
            raise ValueError(constants.ERROR_INVALID_TOKEN)
