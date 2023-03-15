from decimal import Decimal
from math import sin, cos, pow

grid_steps = [Decimal('2'), Decimal('1'), Decimal('0.5'), Decimal('0.25'), Decimal('0.125')]
analyser_start = Decimal('-10')
analyser_end = Decimal('10')


def user_function_trigonometric(x: Decimal) -> Decimal:
    return Decimal(sin(x)) * Decimal(cos(x))


def user_function_trigonometric_actual_derivative(x: Decimal) -> Decimal:
    return Decimal(pow(cos(x), 2)) - Decimal(pow(sin(x), 2))


def user_function_trigonometric_actual_integral(start: Decimal, end: Decimal):
    value = -Decimal('0.5') * Decimal(pow(cos(end), 2))
    if end.compare(start) <= 0:
        return value
    return value - user_function_trigonometric_actual_integral(start, start)


def user_function_quad(x: Decimal) -> Decimal:
    return Decimal('0.25') * Decimal(pow(x, 2)) + x - 3


def user_function_quad_actual_derivative(x: Decimal) -> Decimal:
    return (x + 2) / 2


def user_function_quad_actual_integral(x: Decimal) -> Decimal:
    return Decimal(pow(x, 3)) / 12 + Decimal(pow(x, 2)) / 2 - x * 3
