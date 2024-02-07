import matplotlib.pyplot as plt
import numpy as np

from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, normalize_slanted_field_profile, apply_ppwt_factor, read_roi
from a_etalonnage import od_to_dose
from fit_functions import gaussian_fit, gaussian_function

file_names = ["f) x", "f) y"]
roi_file_names = ["f) x bas", "f) x haut", "f) y gauche", "f) y droite"]
#

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

offset_od_parameter = 0.5
offset_pixel_parameter = 250
top_cm_parameter = 3.5

roi_pixel_lists = []

for roi_file_name in roi_file_names:
    roi_pixel_lists.append(read_roi(roi_file_name))

field_edges = [[], []]
pencil_edges = [[[], []], [[], []]]

for i, file_name in enumerate(file_names):
    raw_pixel_list, gray_list = read_profil(file_name)

    od_list = gray_to_od(gray_list, 115)

    pixel_list = raw_pixel_list
    for index, od in enumerate(od_list):
        if od > offset_od_parameter:
            offset = offset_pixel_parameter - index
            pixel_list = [pixel + offset for pixel in raw_pixel_list]
            break

    cm_array = pixel_to_cm(pixel_list)

    range_100 = []
    for ind, cm in enumerate(cm_array):
        if cm >= top_cm_parameter:
            range_100.append(ind)
            break
    range_100.append(range_100[0] + 1441)

    percent_array = normalize_field_profile(np.array(od_list), range_100)

    plt.scatter(cm_array, percent_array, color=color_list[i], s=0.4, label=file_name[-1])

    for index, percent in enumerate(percent_array):
        if percent >= 50:
            field_edges[i].append(cm_array[index])
            break
    for index, percent in enumerate(reversed(percent_array)):
        if percent >= 50:
            original_index = len(percent_array) - 1 - index
            field_edges[i].append(cm_array[original_index])
            break

    first_roi_list = roi_pixel_lists[2*i]
    second_roi_list = roi_pixel_lists[2*i + 1]

    for number, element in enumerate([first_roi_list, second_roi_list]):
        for stuff in element:
            pencil_edges[i][number].append(cm_array[stuff])

x_gauche_diff = [field_edges[0][0] - pencil_edges[0][0][0], field_edges[0][0] - pencil_edges[0][1][0]]
x_droite_diff = [pencil_edges[0][0][1] - field_edges[0][1], pencil_edges[0][1][1] - field_edges[0][1]]
y_bas_diff = [field_edges[1][0] - pencil_edges[1][0][0], field_edges[1][0] - pencil_edges[1][1][0]]
y_haut_diff = [pencil_edges[1][0][1] - field_edges[1][1], pencil_edges[1][1][1] - field_edges[1][1]]

print(f"x_gauche : {x_gauche_diff}")
print(f"x_droite : {x_droite_diff}")
print(f"y_bas : {y_bas_diff}")
print(f"y_haut : {y_haut_diff}")

plt.legend()
plt.show()
