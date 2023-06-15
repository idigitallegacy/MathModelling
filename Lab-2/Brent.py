import numpy as np
from matplotlib import pyplot as plt
import Setup

threshold = 1

def brent(epsilon, function, a, b):
    iterator = 0
    function_call_iterator = 0
    prev_len = b - a

    a_timelapse = [a]
    b_timelapse = [b]
    ratio_array = []

    d_epsilon = epsilon / 10
    phi = (3 - np.sqrt(5)) / 2
    x = w = v = a + phi * (b - a)
    fx = fw = fv = function(x)
    d = e = b - a

    while d > epsilon:
        g = e
        e = d

        u = None
        if x != w and x != v and w != v and fx != fw and fx != fv and fw != fv:
            p = (x - w) * (fx - fv) - (x - v) * (fx - fw)
            q = 2 * (x - w) * (fx - fv) - 2 * (x - v) * (fx - fw)

            if q != 0:
                u = x - (p / q)
                if a + d_epsilon <= u <= b - d_epsilon and np.abs(u - x) < g / 2:
                    d = np.abs(u - x)
                else:
                    u = None

        if u is None:
            if x < (b + a) / 2:
                u = x + phi * (b - x)
                d = b - x
            else:
                u = x - phi * (x - a)
                d = x - a

            if np.abs(u - x) < d_epsilon:
                u = x + np.sign(u - x) * d_epsilon

        fu = function(u)
        function_call_iterator += 1

        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x

            v, w, x = w, x, u
            fv, fw, fx = fw, fx, fu
        else:
            if u >= x:
                b = u
            else:
                a = u

            if fu <= fw or w == x:
                v, w = w, u
                fv, fw = fw, fu
            elif fu <= fv or v == x:
                v, fv = u, fu

        a_timelapse.append(a), b_timelapse.append(b)
        ratio_array.append(e / d)
        iterator += 1

    return {
        "min": x,
        "iter": iterator,
        "ncalls": function_call_iterator,
        "timelapse": {"start": a_timelapse, "end": b_timelapse},
        "rtime": ratio_array
    }

if __name__ == '__main__':
    result = brent(0.01, Setup.y, 5.0, 8.0)
    print("Минимум осадков в интервале от 5 до 8 в ", str(round(result["min"], 5)), " месяце.")

    # x_scale = [x/1000 for x in range(5000, 8000)]
    # y_plot = [Setup.y(x) for x in x_scale]
    # plt.suptitle("Brent method")
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