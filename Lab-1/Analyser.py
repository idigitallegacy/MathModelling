import numpy as np
from decimal import Decimal
from typing import Callable

import Grid


def mapper(x: Decimal) -> float:
    if x is None:
        return 0.0
    return float(x)


class Analyser:
    def __init__(self,
                 function: Callable[[Decimal], Decimal],
                 derivative_check_function: Callable[[Decimal], Decimal],
                 integral_check_function: Callable[[Decimal, Decimal], Decimal]):
        self.__function = function
        self.__derivative_check_function = derivative_check_function
        self.__integral_check_function = integral_check_function
        self.__derivative_values = None
        self.__integral_values = None
        self.__trusted_step = Decimal('0.01')
        self.__grid = None

    def analyse_derivative(self, start: Decimal, end: Decimal, step: Decimal) -> dict:
        result = {
            "derivative": None,
            "actual_derivative": None,
            "mse": None,
            "analysis_start_value": start,
            "analysis_end_value": end,
            "analysis_step": step
        }

        grid = Grid.Grid((start, end), step)
        derivative = grid.analyse_derivative(self.__function)
        derivative_values = np.array(list(map(mapper, derivative.values())))

        x_values = [start + step * i for i in range(int((end - start) / step))]
        x_values_trusted = [start + self.__trusted_step * i for i in range(int((end - start) / self.__trusted_step))]

        actual_derivative = {x: self.__derivative_check_function(x) for x in x_values}
        actual_derivative_trusted = {x: self.__derivative_check_function(x) for x in x_values_trusted}
        actual_derivative_values = np.array(list(map(mapper, actual_derivative.values())))

        result["derivative"] = derivative
        result["actual_derivative"] = actual_derivative_trusted

        result["mse"] = np.square(np.subtract(derivative_values, actual_derivative_values)).sum() / \
                        int((end - start) / step)
        return result

    def analyse_integral_sum(self, start: Decimal, end: Decimal, step: Decimal, method: str = 's') -> dict:
        result = {
            "integral": None,
            "actual_integral": None,
            "analysis_start_value": start,
            "analysis_end_value": end,
            "analysis_step": step
        }

        grid = Grid.Grid((start, end), step)

        integral = grid.analyse_integral(self.__function, method)
        actual_integral = self.__integral_check_function(start, end)

        result["integral"] = integral
        result["actual_integral"] = actual_integral

        return result
