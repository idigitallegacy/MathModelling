import numpy as np
from matplotlib import pyplot as plt
import Setup

def generate_sequence(min_fibonacci: int) -> list[int]:
    sequence = [1, 1]
    while sequence[-1] <= min_fibonacci:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def fibonacci(epsilon, function, a, b):
    iterator = 0
    function_call_iterator = 0
    prev_len = b - a

    a_timelapse = [a]
    b_timelapse = [b]
    ratio_array = []

    fibonacci_sequence = generate_sequence(np.ceil((b - a) / epsilon))
    n = len(fibonacci_sequence) - 1
    if n < 2:
        x1, x2 = a, b
    else:
        x1, x2 = a + fibonacci_sequence[n - 2] / fibonacci_sequence[n] * (b - a), a + fibonacci_sequence[n - 1] / fibonacci_sequence[n] * (b - a)
    f1, f2 = function(x1), function(x2)
    k = 1
    while k + 2 < n and Setup.is_correct(ratio_array):
        if f1 > f2:
            a = x1
            if n - k < 2:
                x1 = a
            else:
                x1 = a + fibonacci_sequence[n - k - 2] / fibonacci_sequence[n - k] * (b - a)
            x2 = a + fibonacci_sequence[n - k - 1] / fibonacci_sequence[n - k] * (b - a)
            f1, f2 = f2, function(x2)
        else:
            b = x2
            x1 = a + fibonacci_sequence[n - k - 2] / fibonacci_sequence[n - k] * (b - a)
            if n - k < 1:
                x2 = b
            else:
                x2 = a + fibonacci_sequence[n - k - 1] / fibonacci_sequence[n - k] * (b - a)
            f1, f2 = function(x1), f1
        a_timelapse.append(a)
        b_timelapse.append(b)
        iterator += 1
        function_call_iterator += 1
        k += 1
        ratio_array.append(prev_len / (b - a))
        prev_len = b - a
    return {
        "min": (a + b) / 2,
        "iter": iterator,
        "ncalls": function_call_iterator,
        "timelapse": {"start": a_timelapse, "end": b_timelapse},
        "rtime": ratio_array
    }

if __name__ == '__main__':
    result = fibonacci(0.01, Setup.y, 5.0, 8.0)
    print("Минимум осадков в интервале от 5 до 8 в ", str(round(result["min"], 5)), " месяце.")

    # x_scale = [x/1000 for x in range(5000, 8000)]
    # y_plot = [Setup.y(x) for x in x_scale]
    # plt.suptitle("Fibonacci method")
    # plt.plot(x_scale, y_plot, label="Source function")
    # plt.axvline(result["min"], color="magenta", label="Found minimum")
    # plt.ylabel("Precipitation amount")
    # plt.xlabel("Time")
    # plt.legend()
    # plt.show()

    x_scale = [x/10000 for x in range(int(result["min"] * 10000) - 1000, int(result["min"] * 10000) + 1000)]
    y_plot = [Setup.y(x) for x in x_scale]
    plt.suptitle("Fibonacci method")
    plt.plot(x_scale, y_plot, label="Source function")
    plt.axvline(result["min"], color="magenta", label="Found minimum")
    plt.ylabel("Precipitation amount")
    plt.xlabel("Time")
    plt.legend()
    plt.show()

