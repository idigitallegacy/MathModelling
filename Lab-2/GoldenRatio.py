from matplotlib import pyplot as plt
import Setup

def golden_ratio(epsilon, function, a, b):
    golden_const = ((-5 ** 0.5 + 3) / 2)
    golden_const_inv = 1 / ((5 ** 0.5 + 1) / 2)

    iterator = 0
    function_call_iterator = 0
    prev_len = b - a

    a_timelapse = [a]
    b_timelapse = [b]

    ratio_array = []

    saved_part = 0
    prev_func = None
    while b - a > epsilon and Setup.is_correct(ratio_array):
        iterator += 1
        x1 = a + golden_const * (b - a)
        x2 = a + golden_const_inv * (b - a)
        if saved_part == 0:
            f_x1, f_x2 = function(x1), function(x2)
            function_call_iterator += 2
        elif saved_part == -1:
            f_x1, f_x2 = prev_func, function(x2)
            function_call_iterator += 1
        else:
            f_x1, f_x2 = function(x1), prev_func
            function_call_iterator += 1
        if f_x1 < f_x2:
            b = x2
            saved_part = 1
            prev_func = f_x1
        elif f_x1 > f_x2:
            a = x1
            saved_part = -1
            prev_func = f_x2
        else:
            a, b = x1, x2
            saved_part = 0
        ratio_array.append(prev_len / (b - a))
        prev_len = b - a
        a_timelapse.append(a), b_timelapse.append(b)

    return {
        "min": (a + b) / 2,
        "iter": iterator,
        "ncalls": function_call_iterator,
        "timelapse": {"start": a_timelapse, "end": b_timelapse},
        "rtime": ratio_array
    }

if __name__ == '__main__':
    result = golden_ratio(0.01, Setup.y, 5.0, 8.0)
    print("Минимум осадков в интервале от 5 до 8 в ", str(round(result["min"], 5)), " месяце.")

    # x_scale = [x/1000 for x in range(5000, 8000)]
    # y_plot = [Setup.y(x) for x in x_scale]
    # plt.suptitle("Golden ratio method")
    # plt.plot(x_scale, y_plot, label="Source function")
    # plt.axvline(result["min"], color="magenta", label="Found minimum")
    # plt.ylabel("Precipitation amount")
    # plt.xlabel("Time")
    # plt.legend()
    # plt.show()

    x_scale = [x/10000 for x in range(int(result["min"] * 10000) - 1000, int(result["min"] * 10000) + 1000)]
    y_plot = [Setup.y(x) for x in x_scale]
    plt.suptitle("Golden ratio method")
    plt.plot(x_scale, y_plot, label="Source function")
    plt.axvline(result["min"], color="magenta", label="Found minimum")
    plt.ylabel("Precipitation amount")
    plt.xlabel("Time")
    plt.legend()
    plt.show()