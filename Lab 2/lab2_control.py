import matplotlib.pyplot as plt
import numpy as np
from profil_functions import read_profil, read_roi_inch, smooth, cut_replace
from lab2_0_etalonnage import zero_pixel_value
from fit_functions import quadratic_fit, quadratic_function

file_name = "controle"
problems = [[2060, 2062]]

go_smooth = True
smooth_range = 55
cut_range = int((smooth_range - 1)/2)

raw_inch_list, raw_gray_list = read_profil(file_name, distance='Distance_(inches)')
repaired_gray_list = cut_replace(np.array(raw_inch_list), np.array(raw_gray_list), problems)
cut_indexes = read_roi_inch(file_name)
start, end = cut_indexes[0], cut_indexes[1]
short_inch_list, short_gray_list = raw_inch_list[start:end], repaired_gray_list[start:end]

plt.scatter(short_inch_list, short_gray_list, s=0.7, color="r")
# plt.scatter(raw_inch_list, repaired_gray_list, s=1.2, color="b")

if go_smooth:
    short_gray_list = smooth(short_gray_list, smooth_range)
    short_inch_list = short_inch_list[cut_range:-cut_range]

params, cov = quadratic_fit(short_inch_list, short_gray_list)
a, b, c = params[0], params[1], params[2]


def control_calibration(x_list, gray_list):

    return gray_list + zero_pixel_value() - quadratic_function(x_list, a, b, c)


calibrated_gray_array = control_calibration(np.array(short_inch_list), np.array(short_gray_list))

if __name__ == "__main__":
    plt.plot(raw_inch_list, quadratic_function(np.array(raw_inch_list), a, b, c))
    plt.scatter(raw_inch_list, raw_gray_list, s=0.3, color="g")
    plt.plot([0, 9], [zero_pixel_value(), zero_pixel_value()])
    plt.scatter(short_inch_list, calibrated_gray_array, s=0.3, color="r")

    plt.show()
