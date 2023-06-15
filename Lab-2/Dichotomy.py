from matplotlib import pyplot as plt
import Setup

def dichotomy(epsilon, function, a, b):
    iterator = 0
    function_call_iterator = 0
    prev_len = b - a

    a_timelapse = [a]
    b_timelapse = [b]

    ratio_array = []

    while b - a > epsilon and Setup.is_correct(ratio_array):
        iterator += 1

        x1 = (a + b) / 2 - epsilon / 2
        x2 = (a + b) / 2 + epsilon / 2

        f_x1 = function(x1)
        f_x2 = function(x2)

        function_call_iterator += 2

        if f_x1 < f_x2:
            b = x2
        elif f_x1 > f_x2:
            a = x1
        else:
            a, b = x1, x2

        a_timelapse.append(a)
        b_timelapse.append(b)
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
    result = dichotomy(0.01, Setup.y, 5.0, 8.0)
    print("Минимум осадков в интервале от 5 до 8 в ", str(round(result["min"], 5)), " месяце.")

    # x_scale = [x/1000 for x in range(5000, 8000)]
    # y_plot = [Setup.y(x) for x in x_scale]
    # plt.suptitle("Dichotomy method")
    # plt.plot(x_scale, y_plot, label="Source function")
    # plt.axvline(result["min"], color="magenta", label="Found minimum")
    # plt.ylabel("Precipitation amount")
    # plt.xlabel("Time")
    # plt.legend()
    # plt.show()

    x_scale = [x/10000 for x in range(int(result["min"] * 10000) - 1000, int(result["min"] * 10000) + 1000)]
    y_plot = [Setup.y(x) for x in x_scale]
    plt.suptitle("Dichotomy method")
    plt.plot(x_scale, y_plot, label="Source function")
    plt.axvline(result["min"], color="magenta", label="Found minimum")
    plt.ylabel("Precipitation amount")
    plt.xlabel("Time")
    plt.legend()
    plt.show()