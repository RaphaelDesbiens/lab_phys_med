import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, smooth, normalize_slanted_field_profile, apply_ppwt_factor
from a_etalonnage import od_to_dose
from fit_functions import linear_fit
import numpy as np

file_names = ["c) px", "c) py", "c) dx", "c) dy"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']
curve_names = ["Physique (x)", "Physique (y)", "Dynamique (x)", "Dynamique (y)"]

offset_od_parameter = 0.29
offset_pixel_parameter = 250
top_cm_parameter = 3.5
go_smooth = True
smooth_range = 5
cut_range = int((smooth_range - 1)/2)
slanted_mean_range = 60
top_doze_10cm_b_200MU = 2.37      # Gy
top_doze_10cm_b_250MU = 2.5*top_doze_10cm_b_200MU/2

od_profiles = []
for file_name in file_names:
    pixel_list, gray_list = read_profil(file_name)
    full_pixel_list = pixel_list
    rough_gray_list = gray_list
    if go_smooth:
        gray_list = smooth(rough_gray_list, smooth_range)
        pixel_list = full_pixel_list[cut_range:-cut_range]

    od_list = gray_to_od(gray_list)
    od_profiles.append([pixel_list, od_list])

for index, od_profil in enumerate(od_profiles):
    raw_pixel_list = od_profil[0]
    od_list = od_profil[1]
    pixel_list = []
    for i, od in enumerate(od_list):
        if od > offset_od_parameter:
            offset = offset_pixel_parameter - i
            pixel_list = [pixel + offset for pixel in raw_pixel_list]
            break
    cm_array = apply_ppwt_factor(pixel_to_cm(pixel_list))
    dose_array = od_to_dose(od_list)

    percent_array, top_doze = None, None
    if file_names[index][-1] == "x":
        range_100 = []
        for ind, cm in enumerate(cm_array):
            if cm >= top_cm_parameter:
                range_100.append(ind)
                break
        range_100.append(range_100[0] + 1120)
        percent_array, top_doze = normalize_field_profile(dose_array, range_100)
    else:
        percent_array, top_doze = normalize_slanted_field_profile(dose_array, slanted_mean_range)
        slanted_field_edges = measure_field_size(cm_array, percent_array)
        slanted_field_size = slanted_field_edges[1] - slanted_field_edges[0]
        slanted_field_left = slanted_field_edges[0] + 0.05 * slanted_field_size
        slanted_field_right = slanted_field_edges[1] - 0.05 * slanted_field_size
        slanted_field_indexes = []
        for i, cm in enumerate(cm_array):
            if cm > slanted_field_left:
                slanted_field_indexes.append(i)
                break
        for i, cm in enumerate(cm_array):
            if cm > slanted_field_right:
                slanted_field_indexes.append(i - 1)
                break
        slanted_percent_array = percent_array[slanted_field_indexes[0]:slanted_field_indexes[1]]
        slanted_cm_array = cm_array[slanted_field_indexes[0]:slanted_field_indexes[1]]
        params, covariance = linear_fit(slanted_cm_array, slanted_percent_array)
        m, b = params[0], params[1]
        x_values = np.array([cm_array[slanted_field_indexes[0]], cm_array[slanted_field_indexes[1]]])
        y_values = m*x_values + b
        print(f"m = {m}")

        middle_cm_index = int((slanted_field_indexes[0] + slanted_field_indexes[1])/2)
        middle_cm = cm_array[middle_cm_index]
        middle_percent = m*middle_cm + b
        middle_dose = top_doze*middle_percent/100
        wedge_factor = middle_dose / top_doze_10cm_b_250MU
        print(f"middle_dose = {middle_dose}")
        print(f"wedge_factor = {wedge_factor}")

    cm_array = cm_array - 9.8
    plt.scatter(cm_array, percent_array, color=color_list[index], s=1, label=curve_names[index])

plt.legend()
plt.xlabel("Distance avec l'isocentre (cm)")
plt.ylabel(r'Dose normalisée (D/D$_{max}$)')
plt.ylim(bottom=0)
plt.show()