import math
import pytest
from calculator import Calculator

calc = Calculator()


# === БАЗОВЫЕ ОПЕРАЦИИ ===
@pytest.mark.parametrize("expr,expected", [
    ("2+3", 5),
    ("10-3", 7),
    ("4*5", 20),
    ("15/3", 5),
    ("2^3", 8),
])
def test_basic_operations(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === ПРОБЕЛЫ, СКОБКИ, ОТРИЦАТЕЛЬНЫЕ ===
@pytest.mark.parametrize("expr,expected", [
    ("2 + 3", 5),
    ("(2+3)*4", 20),
    ("-5+10", 5),
    ("(3-5)*-2", 4),
    ("((2+3)*(4+1))", 25),
])
def test_spaces_and_parentheses(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === ДЕСЯТИЧНЫЕ ===
@pytest.mark.parametrize("expr,expected", [
    ("2.5+3.5", 6),
    ("0.1*10", 1),
    ("3.14*2", 6.28),
])
def test_decimals(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === ОШИБКИ ===
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calc.evaluate("10/0")


@pytest.mark.parametrize("expr", [
    "2++3",
    "(", 
    "sqrt(-4)",
    "log(0)",
    "foo(2)"
])
def test_invalid_and_math_errors(expr):
    with pytest.raises(ValueError):
        calc.evaluate(expr)


# === ПОРЯДОК ОПЕРАЦИЙ ===
@pytest.mark.parametrize("expr,expected", [
    ("2+3*4", 14),
    ("(2+3)*4", 20),
    ("2^3^2", 512), 
])
def test_operator_precedence(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === ФУНКЦИИ И ГРАДУСЫ ===
@pytest.mark.parametrize("expr,expected", [
    ("sin(pi/2)", 1.0),
    ("cos(0)", 1.0),
    ("tan(pi/4)", 1.0),
    ("sin(90deg)", 1.0),
    ("cos(180deg)", -1.0),
    ("tan(45deg)", 1.0),
    ("sqrt(16)", 4.0),
    ("log(e)", 1.0),
    ("exp(1)", math.e),
])
def test_functions(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === ВЛОЖЕННЫЕ ФУНКЦИИ ===
@pytest.mark.parametrize("expr,expected", [
    ("sin(cos(0))", math.sin(math.cos(0))),
    ("sqrt(sin(pi/2)+cos(0))", math.sqrt(math.sin(math.pi/2)+math.cos(0))),
    ("log(exp(1))", 1),
])
def test_nested_functions(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)


# === СЛОЖНЫЕ ВЫРАЖЕНИЯ ===
@pytest.mark.parametrize("expr,expected", [
    ("((2+3)*4)^2", 400),
    ("(2^3)+(4^2)", 24),
    ("exp(log(e^2))", math.e**2),
    ("sqrt((3^2)+(4^2))", 5),  
])
def test_complex_expressions(expr, expected):
    assert calc.evaluate(expr) == pytest.approx(expected, rel=1e-9)
