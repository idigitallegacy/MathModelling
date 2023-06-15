from matplotlib import pyplot as plt
import Brent, Dichotomy, Fibonacci, GoldenRatio, Parabolic
import Setup

x_values = [1/x for x in range(10, 10000)]
y_brent_values = [Brent.brent(x, Setup.y, 0, 12)["ncalls"] for x in x_values]
y_dichotomy_values = [Dichotomy.dichotomy(x, Setup.y, 0, 12)["ncalls"] for x in x_values]
y_fibonacci_values = [Fibonacci.fibonacci(x, Setup.y, 0, 12)["ncalls"] for x in x_values]
y_golden_ratio_values = [GoldenRatio.golden_ratio(x, Setup.y, 0, 12)["ncalls"] for x in x_values]
y_parabolic_values = [Parabolic.parabolic(x, Setup.y, 0, 12)["ncalls"] for x in x_values]

plt.suptitle("Methods comparison by function calls with given precision")
plt.xlabel("Precision")
plt.ylabel("Function calls amount")
plt.plot(x_values, y_brent_values, label="Brent's")
plt.plot(x_values, y_dichotomy_values, label="Dichotomy")
plt.plot(x_values, y_fibonacci_values, label="Fibonacci")
plt.plot(x_values, y_golden_ratio_values, label="Golden ratio")
plt.plot(x_values, y_parabolic_values, label="Parabolic")
plt.semilogx()
plt.legend()
plt.show()