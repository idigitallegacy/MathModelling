from decimal import Decimal
from matplotlib import pyplot as plt
import Analyser
import Setup


def plot_two_derivatives(actual: dict, estimated: dict, name) -> None:
    plt.title('Derivative deviation', fontsize=15)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('Derivative', fontsize=12)
    plt.plot(list(map(mapper, actual.keys())), list(map(mapper, actual.values())), '-', label='Actual derivative')
    plt.plot(list(map(mapper, estimated.keys())), list(map(mapper, estimated.values())), '--', label='Estimated derivative')

    plt.legend()
    plt.grid(True)
    plt.savefig('./plots/' + name + ".png")
    plt.close()


def plot_mse_dependency(dependency: dict, name) -> None:
    plt.title('MSE Dependency from grid step', fontsize=15)
    plt.xlabel('Grid step', fontsize=12)
    plt.ylabel('MSE', fontsize=12)
    plt.plot(list(map(mapper, dependency.keys())), list(map(mapper, dependency.values())))
    plt.grid(True)
    plt.savefig('./plots/' + name + ".png")
    plt.close()


def plot_integral_offset(offset: dict, name) -> None:
    plt.title('Integral offset from grid step', fontsize=15)
    plt.xlabel('Grid step', fontsize=12)
    plt.ylabel('Offset', fontsize=12)
    plt.plot(list(map(mapper, offset.keys())), list(map(mapper, offset.values())))
    plt.grid(True)
    plt.savefig('./plots/' + name + ".png")
    plt.close()


def mapper(x: Decimal) -> float:
    if x is None:
        return 0.0
    return float(x)


if __name__ == '__main__':
    derivative_mse = {
        "trigonometric": {},
        "quad": {},
    }
    integral_offset = {
        "trigonometric": {},
        "quad": {},
    }
    for grid_step in Setup.grid_steps:
        trigonometric_analyser = Analyser.Analyser(Setup.user_function_trigonometric,
                                                   Setup.user_function_trigonometric_actual_derivative,
                                                   Setup.user_function_trigonometric_actual_integral)

        analysed_derivative = trigonometric_analyser.analyse_derivative(Setup.analyser_start, Setup.analyser_end, grid_step)
        plot_two_derivatives(analysed_derivative["actual_derivative"], analysed_derivative["derivative"], "trigonometric_step_" + str(grid_step))
        derivative_mse["trigonometric"][str(grid_step)] = analysed_derivative["mse"]

        analysed_integral = trigonometric_analyser.analyse_integral_sum(Setup.analyser_start, Setup.analyser_end, grid_step)
        integral_offset["trigonometric"][str(grid_step)] = abs(analysed_integral["integral"] - analysed_integral["actual_integral"])

        quad_analyser = Analyser.Analyser(Setup.user_function_quad,
                                          Setup.user_function_quad_actual_derivative,
                                          Setup.user_function_quad_actual_integral)

        analysed_derivative = quad_analyser.analyse_derivative(Setup.analyser_start, Setup.analyser_end, grid_step)
        plot_two_derivatives(analysed_derivative["actual_derivative"], analysed_derivative["derivative"], "quad_step_" + str(grid_step))
        derivative_mse["quad"][str(grid_step)] = analysed_derivative["mse"]

        analysed_integral = trigonometric_analyser.analyse_integral_sum(Setup.analyser_start, Setup.analyser_end, grid_step)
        integral_offset["quad"][str(grid_step)] = abs(analysed_integral["integral"] - analysed_integral["actual_integral"])

    plot_mse_dependency(derivative_mse["trigonometric"], "trigonometric_mse_dependency")
    plot_mse_dependency(derivative_mse["quad"], "quad_mse_dependency")
    plot_integral_offset(integral_offset["trigonometric"], "trigonometric_integral_offset")
    plot_integral_offset(integral_offset["quad"], "quad_integral_offset")