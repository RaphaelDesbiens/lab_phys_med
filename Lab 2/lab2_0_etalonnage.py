import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od
from fit_functions import linear_fit_b, linear_function_b
from statistics import mean
import numpy as np

file_names = ['etalonnage_0Gy',
              'etalonnage_0.25Gy',
              'etalonnage_0.5Gy',
              'etalonnage_1Gy',
              'etalonnage_1.5Gy',
              'etalonnage_2Gy',
              'etalonnage_3Gy',
              'etalonnage_4Gy',
              'etalonnage_5Gy']

doses = [0, 0.25, 0.5, 1, 1.5, 2, 3, 4, 5]

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA', u'#FA8072', u'#FDF5E6', u'#FFDAB9', u'#FFA07A', u'#D2691E',
    u'#CD853F', u'#F4A460', u'#8B4513', u'#A0522D', u'#A52A2A', u'#800000', u'#FFFFFF', u'#F5F5F5'
    ]

od_values = []
zero_value = None

for i, file_name in enumerate(file_names):
    raw_pixel_list, raw_gray_list = read_profil(file_name)
    gray_value = mean(raw_gray_list)
    # print(f"{file_name[11:]} --> {(gray_value + 1)*256 - 1}")
    if i == 0:
        zero_value = (gray_value+1)*256 - 1
    od_value = gray_to_od(gray_value, 255)
    od_values.append(od_value)

params, cov = linear_fit_b(doses[:-1], od_values[:-1])
m, sigma_m = params[0], np.sqrt(cov[0][0])


def zero_pixel_value():

    return zero_value


def calibrate(od_array):

    return (od_array - od_values[0]) / m


if __name__ == "__main__":

    print(f"OD = ({m:.4f} +/- {sigma_m:.4f})D + 0.18181836")

    plt.scatter(doses, od_values)

    x_values = np.array([-0.5, 5.5])
    y_values = linear_function_b(x_values, m)
    plt.plot(x_values, y_values)

    plt.show()
