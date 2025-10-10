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