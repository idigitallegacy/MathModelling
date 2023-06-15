from matplotlib import pyplot as plt
import numpy as np
import Brent, Dichotomy, Fibonacci, GoldenRatio, Parabolic
import Setup


brent = Brent.brent(0.0001, Setup.y, 0, 12)
x_brent_values = [x for x in range(len(brent["timelapse"]["start"]))]
y_brent_values = np.subtract(brent["timelapse"]["end"], brent["timelapse"]["start"])

dichotomy = Dichotomy.dichotomy(0.0001, Setup.y, 0, 12)
x_dichotomy_values = [x for x in range(len(dichotomy["timelapse"]["start"]))]
y_dichotomy_values = np.subtract(dichotomy["timelapse"]["end"], dichotomy["timelapse"]["start"])

fibonacci = Fibonacci.fibonacci(0.0001, Setup.y, 0, 12)
x_fibonacci_values = [x for x in range(len(fibonacci["timelapse"]["start"]))]
y_fibonacci_values = np.subtract(fibonacci["timelapse"]["end"], fibonacci["timelapse"]["start"])

golden_ratio = GoldenRatio.golden_ratio(0.0001, Setup.y, 0, 12)
x_golden_ratio_values = [x for x in range(len(golden_ratio["timelapse"]["start"]))]
y_golden_ratio_values = np.subtract(golden_ratio["timelapse"]["end"], golden_ratio["timelapse"]["start"])

parabolic = Parabolic.parabolic(0.0001, Setup.y, 0, 12)
x_parabolic_values = [x for x in range(len(parabolic["timelapse"]["start"]))]
y_parabolic_values = np.subtract(parabolic["timelapse"]["end"], parabolic["timelapse"]["start"])

plt.suptitle("Methods comparison by section length with epsilon = 0.0001")
plt.xlabel("Iteration")
plt.ylabel("Section length")
plt.plot(x_brent_values, y_brent_values, label="Brent's")
plt.plot(x_dichotomy_values, y_dichotomy_values, label="Dichotomy")
plt.plot(x_fibonacci_values, y_fibonacci_values, label="Fibonacci")
plt.plot(x_golden_ratio_values, y_golden_ratio_values, label="Golden ratio")
plt.plot(x_parabolic_values, y_parabolic_values, label="Parabolic")
plt.legend()
plt.show()