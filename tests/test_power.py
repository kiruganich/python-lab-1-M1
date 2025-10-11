import pytest

from src.power import evaluate


def test_basic_operations():
    assert evaluate("2+3") == 5
    assert evaluate("5-2") == 3
    assert evaluate("4*3") == 12
    assert evaluate("10/2") == 5.0


# Приоритеты
def test_operator_precedence():
    assert evaluate("2+3*4") == 14
    assert evaluate("10-2*3") == 4


# Скобки
def test_parentheses():
    assert evaluate("(2+3)*4") == 20
    assert evaluate("2*(3+4)") == 14


def test_unary_operators():
    assert evaluate("-5") == -5
    assert evaluate("--5") == 5
    assert evaluate("-(2+3)") == -5
    assert evaluate("+5") == 5


# Возведение в степень - правоассоциативная функция
def test_power_operator():
    assert evaluate("2**3") == 8
    assert evaluate("2**3**2") == 512


# Деление нацело без остатка с целыми числами
def test_floor_division_and_modulo_with_integers():
    assert evaluate("7//2") == 3
    assert evaluate("7%2") == 1
    assert evaluate("10//3") == 3
    assert evaluate("10%3") == 1


def test_float_operations():
    result = evaluate("3.5+2.1")
    assert abs(result - 5.6) < 1e-10


def test_division_by_zero():
    with pytest.raises(ValueError, match="E2: Деление на ноль"):
        evaluate("5/0")

    with pytest.raises(ValueError, match="E2: Деление на ноль"):
        evaluate("5//0")

    with pytest.raises(ValueError, match="E2: Деление на ноль"):
        evaluate("5%0")


# Деление нацело без остатка с нецелыми числами
def test_floor_div_mod_with_float_raises_error():
    with pytest.raises(ValueError, match="// только для целых чисел"):
        evaluate("5//2.0")

    with pytest.raises(ValueError, match="только для целых"):
        evaluate("7.0//2")

    with pytest.raises(ValueError, match="только для целых"):
        evaluate("5%2.0")

    with pytest.raises(ValueError, match="только для целых"):
        evaluate("7%2.5")


# Синтаксические ошибки
def test_syntax_errors():
    # Лишний символ в конце - это неожиданный конец, а не недопустимый токен
    with pytest.raises(ValueError, match="E3: Неожиданный конец выражения"):
        evaluate("2+")

    with pytest.raises(ValueError, match="E4: Несогласованные скобки"):
        evaluate("(2+3")
