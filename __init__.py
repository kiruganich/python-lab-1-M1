from src.power import evaluate

def test_basic_operations():
    assert evaluate("2+3") == 5
    assert evaluate("10-4") == 6
    assert evaluate("3*4") == 12
    assert evaluate("8/2") == 4.0

def test_operator_precedence():
    assert evaluate("2+3*4") == 14
    assert evaluate("10-2*3") == 4

def test_parentheses():
    assert evaluate("(2+3)*4") == 20
    assert evaluate("2*(3+4)") == 14

def test_unary_operators():
    assert evaluate("-5") == -5
    assert evaluate("--5") == 5
    assert evaluate("-(2+3)") == -5
    assert evaluate("+5") == 5

def test_power_operator():
    assert evaluate("2**3") == 8
    assert evaluate("2**3**2") == 512  #2**(3**2)

def test_floor_division_and_modulo():
    assert evaluate("7//2") == 3
    assert evaluate("7%2") == 1
    assert evaluate("10//3") == 3

def test_float_numbers():
    assert abs(evaluate("3.5 + 2.1") - 5.6) < 1e-10

def test_division_by_zero():
    try:
        evaluate("5/0")
        assert False, "Должна быть ошибка деления на ноль"
    except ValueError as e:
        assert "Деление на ноль" in str(e)

def test_floor_div_for_float():
    try:
        evaluate("5.0//2")
        assert False, "Оператор // должен работать только с целыми"
    except ValueError as e:
        assert "только для целых" in str(e)

def test_mismatched_parentheses():
    try:
        evaluate("(2+3")
        assert False, "Должна быть ошибка скобок"
    except ValueError as e:
        assert "скобки" in str(e)

def test_invalid_characters():
    try:
        evaluate("2+3a")
        assert False, "Должна быть ошибка недопустимого символа"
    except ValueError as e:
        assert "Недопустимый токен" in str(e)