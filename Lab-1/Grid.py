from decimal import Decimal
import copy
from typing import Callable, Tuple


class Grid:
    def __init__(self, grid_range: Tuple[Decimal, Decimal], grid_step: Decimal):
        if grid_range[0].compare(grid_range[1]) >= 0 or (grid_range[1] - grid_range[0] - 3 * grid_step).compare(0) < 0:
            raise ValueError("Invalid grid range or grid: empty grid given or it consists of less than 3 cells.")
        if grid_step.compare(0) < 0:
            raise ValueError("Invalid grid step: it must be above zero.")
        self.__grid_range = grid_range
        self.__grid_step = grid_step
        self.__cells_amount = int((grid_range[1] - grid_range[0]) / grid_step)
        self.__grid = [grid_range[0] + grid_step * i for i in range(self.__cells_amount)]
        self.__function_values = {}
        self.__derivative_values = {}
        self.__integral_values = {}
        self.__previously_analyzed = None

    def __mapper(self, x: Decimal | None) -> Decimal:
        if x is None:
            return Decimal('0.0')
        return x

    def __calculate_function_values(self, func: Callable[[Decimal], Decimal]) -> None:
        # calculates 2 * self.__grid_step values of a function to use
        # 'f_1/2(x)' [[ asserting function is being analysed on a
        # subgrid of a supergrid, scaled down 4 times by square ]]
        supergrid = [self.__grid_range[0] + self.__grid_step * i / 2 for i in range(2 * self.__cells_amount)]
        for x in supergrid:
            self.__function_values[x] = func(x)

    def __elementary_derivative(self, grid_x: Decimal) -> Decimal:
        if (grid_x - self.__grid_step).compare(self.__grid_range[0]) < 0:
            return (-3 * self.__function_values[self.__grid[0]] + 4 * self.__function_values[self.__grid[1]]
                    - self.__function_values[self.__grid[2]])\
                   / (2 * self.__grid_step)
        if (grid_x + self.__grid_step).compare(self.__grid_range[1] - self.__grid_step) > 0:
            return (self.__function_values[self.__grid[self.__cells_amount - 3]] -
                    4 * self.__function_values[self.__grid[self.__cells_amount - 2]] +
                    3 * self.__function_values[self.__grid[self.__cells_amount - 1]]) /\
                   (2 * self.__grid_step)
        return (self.__function_values[grid_x + self.__grid_step] -
                self.__function_values[grid_x - self.__grid_step]) /\
               (2 * self.__grid_step)

    def __right_rectangle_elementary_integral(self, grid_x: Decimal) -> Decimal:
        return self.__grid_step * self.__function_values[grid_x]

    def __middle_rectangle_elementary_integral(self, grid_x: Decimal) -> Decimal:
        return self.__grid_step * self.__function_values[grid_x - self.__grid_step / 2]

    def __left_rectangle_elementary_integral(self, grid_x: Decimal) -> Decimal:
        if (grid_x - self.__grid_step).compare(self.__grid_range[0]) < 0:
            return self.__right_rectangle_elementary_integral(grid_x)
        return self.__grid_step * self.__function_values[grid_x - self.__grid_step]

    def __trapezium_elementary_integral(self, grid_x: Decimal) -> Decimal | None:
        if (grid_x - self.__grid_step).compare(self.__grid_range[0]) < 0:
            return None
        return (self.__grid_step / 2) * \
               (self.__function_values[grid_x - self.__grid_step] + self.__function_values[grid_x])

    def __simpson_elementary_integral(self, grid_x: Decimal) -> Decimal | None:
        if (grid_x - self.__grid_step).compare(self.__grid_range[0]) < 0:
            return None
        return (self.__grid_step / 6) * \
               (self.__function_values[grid_x - self.__grid_step] +
                4 * self.__function_values[grid_x - self.__grid_step / 2] +
                self.__function_values[grid_x])

    def __find_derivative(self):
        for x in self.__grid:
            self.__derivative_values[x] = self.__elementary_derivative(x)

    def __find_integral(self, method: Callable[[Decimal], Decimal]) -> None:
        for x in self.__grid:
            self.__integral_values[x] = method(x)

    def analyse_derivative(self, function: Callable[[Decimal], Decimal]) -> dict:
        if self.__previously_analyzed != function:
            self.clear()
            self.__previously_analyzed = function
            self.__calculate_function_values(function)
        else:
            return copy.deepcopy(self.__derivative_values)
        self.__find_derivative()
        return copy.deepcopy(self.__derivative_values)

    def analyse_integral(self, function: Callable[[Decimal], Decimal], method: str = "s") -> Decimal:
        if self.__previously_analyzed != function:
            self.clear()
            self.__previously_analyzed = function
            self.__calculate_function_values(function)
        else:
            return sum(list(map(self.__mapper, self.__integral_values.values())))
        match method:
            case 'rr':
                self.__find_integral(self.__right_rectangle_elementary_integral)
            case 'mr':
                self.__find_integral(self.__middle_rectangle_elementary_integral)
            case 'lr':
                self.__find_integral(self.__left_rectangle_elementary_integral)
            case 't':
                self.__find_integral(self.__trapezium_elementary_integral)
            case 's':
                self.__find_integral(self.__simpson_elementary_integral)
            case _:
                print("Undefined integral method provided: used 'right-rectangle' ('rr') instead.")
                self.__find_integral(self.__right_rectangle_elementary_integral)
        return sum(list(map(self.__mapper, self.__integral_values.values())))

    def clear(self) -> None:
        self.__function_values.clear()
        self.__derivative_values.clear()
        self.__integral_values.clear()
        self.__previously_analyzed = None
