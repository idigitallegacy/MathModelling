from matplotlib import pyplot as plt
import Setup

def parabolic(epsilon, function, a, b):
    iterator = 0
    function_call_iterator = 0
    prev_len = b - a

    a_timelapse = [a]
    b_timelapse = [b]

    ratio_array = []

    x1, x2, x3 = a, (b + a) / 2, b
    f1, f2, f3 = function(x1), function(x2), function(x3)
    while True:
        iterator += 1
        numerator = ((x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1))
        denominator = 2 * ((x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1))
        if denominator == 0 or abs(x3 - x1) < epsilon or not Setup.is_correct(ratio_array):
            break
        x_min = x2 - numerator / denominator
        f_min = function(x_min)

        if x_min < x2:
            if f_min > f2:
                x1 = x_min
                f1 = f_min
            else:
                x3, x2 = x2, x_min
                f3, f2 = f2, f_min
        else:
            if f_min > f2:
                x3 = x_min
                f3 = f_min
            else:
                x1, x2 = x2, x_min
                f1, f2 = f2, f_min

        function_call_iterator += 1
        a_timelapse.append(x1)
        b_timelapse.append(x3)
        ratio_array.append(prev_len / (x3 - x1))
        prev_len = x3 - x1
    if x2 == x1 or f2 == f1:
        return {
        "min": a_timelapse[-1],
        "iter": iterator,
        "ncalls": function_call_iterator,
        "timelapse": {"start": a_timelapse, "end": b_timelapse},
        "rtime": ratio_array
    }
    return {
        "min": b_timelapse[-1],
        "iter": iterator,
        "ncalls": function_call_iterator,
        "timelapse": {"start": a_timelapse, "end": b_timelapse},
        "rtime": ratio_array
    }

if __name__ == '__main__':
    result = parabolic(0.01, Setup.y, 5.0, 8.0)
    print("Минимум осадков в интервале от 5 до 8 в ", str(round(result["min"], 5)), " месяце.")

    # x_scale = [x/1000 for x in range(5000, 8000)]
    # y_plot = [Setup.y(x) for x in x_scale]
    # plt.suptitle("Parabolic method")
    # plt.plot(x_scale, y_plot, label="Source function")
    # plt.axvline(result["min"], color="magenta", label="Found minimum")
    # plt.ylabel("Precipitation amount")
    # plt.xlabel("Time")
    # plt.legend()
    # plt.show()

    x_scale = [x/10000 for x in range(int(result["min"] * 10000) - 1000, int(result["min"] * 10000) + 1000)]
    y_plot = [Setup.y(x) for x in x_scale]
    plt.suptitle("Parabolic method")
    plt.plot(x_scale, y_plot, label="Source function")
    plt.axvline(result["min"], color="magenta", label="Found minimum")
    plt.ylabel("Precipitation amount")
    plt.xlabel("Time")
    plt.legend()
    plt.show()