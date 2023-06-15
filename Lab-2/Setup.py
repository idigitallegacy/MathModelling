import numpy as np

threshold = 1

def y(x):
    if x < 0.0:
        return y(x + 12.0)
    elif x <= 12.0:
        return np.power(x, np.sin(x))
    else:
        return y(x - 12.0)

def is_correct(ratio_array):
  return len(ratio_array) < 1 or ratio_array[-1] > threshold