import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from fit_functions import linear_fit, linear_function
from profil_functions import read_profil, read_roi, gray_to_od

file_name = "Profil des carrés 2x2"

dose_list = [5, 4, 3, 2, 1.5, 1, 0.5, 0.25, 0]

pixel_list, gray_list = read_profil(file_name)
roi_pixel_list = read_roi(file_name)

film_gray_values = []
for film_index in range(int(len(roi_pixel_list)/2)):
    start_index = 2*film_index
    end_index = 2*film_index + 1
    start = int(roi_pixel_list[start_index])
    end = int(roi_pixel_list[end_index])
    film_gray_list = gray_list[start:end]
    mean_gray_value = stat.mean(film_gray_list)
    film_gray_values.append(mean_gray_value)
    # print(mean_gray_value)

optical_densities = gray_to_od(film_gray_values)

od_zero_fix = optical_densities[-1]

params, covariance = linear_fit(dose_list[1:], optical_densities[1:], intercept=True)
m = params[0]


def od_to_dose(od_list):
    return np.array([(od - od_zero_fix)/m for od in od_list])


if __name__ == "__main__":

    x_values = np.array([0, 4])
    y_values = linear_function(x_values, m, od_zero_fix)
    x_dash = np.array([-0.5, 5.5])
    y_dash = linear_function(x_dash, m, od_zero_fix)

    plt.figure(figsize=(10, 5))
    plt.scatter(dose_list, optical_densities, marker='o', color='b', zorder=5)
    plt.plot(x_values, y_values, color='red', zorder=10)
    plt.plot(x_dash, y_dash, '--', color='red', zorder=10, linewidth=0.5)

    plt.title("Courbe d'étalonnage de la densité optique des films EBT3 en fonction de la dose absorbée")
    plt.xlabel('Dose (Gy)')
    plt.ylabel('Densité optique')

    plt.grid(True, color='lightgrey', linestyle='--', linewidth=0.5, zorder=0)

    plt.show()
