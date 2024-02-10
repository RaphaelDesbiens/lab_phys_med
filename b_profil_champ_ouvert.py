import matplotlib.pyplot as plt
import numpy as np
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, apply_ppwt_factor
from a_etalonnage import od_to_dose

file_names = ["b) 1x", "b) 1y", "b) 2x", "b) 2y"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']
curve_names = [r"d$_{max}$ (x)", r"d$_{max}$ (y)", r"10 cm (x)", r"10 cm (y)"]

offset_od_parameter = 0.33
offset_pixel_parameter = 250
top_cm_parameter = 3.5
go_smooth = True
smooth_range = 5
cut_range = int((smooth_range - 1)/2)

low_percent_pen_list = [35, 35, 35, 35]
high_percent_pen_list =[80, 80, 80, 80]

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

field_size_list = []
penumbra_list = []
plt.figure(figsize=(10, 5))
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

    range_100 = []
    for ind, cm in enumerate(cm_array):
        if cm >= top_cm_parameter:
            range_100.append(ind)
            break
    range_100.append(range_100[0] + 1000)

    percent_array, top_dose = normalize_field_profile(dose_array, range_100)
    print(f"top_dose = {top_dose}")

    field_edges = measure_field_size(cm_array, percent_array)
    field_size = field_edges[1] - field_edges[0]
    print(f"field_size = {field_size:.2f}")
    field_size_list.append(field_size)

    low_percent_pen = low_percent_pen_list[index]
    high_percent_pen = high_percent_pen_list[index]
    left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [low_percent_pen, high_percent_pen])
    penumbra_list.append([left_penumbra, right_penumbra])
    print(f"left_penumbra = {left_penumbra:.2f}")
    print(f"right_penumbra = {right_penumbra:.2f}")

    homog_field_left = field_edges[0] + 0.1*field_size
    homog_field_right = field_edges[1] - 0.1 * field_size
    homog_field_indexes = []
    for i, cm in enumerate(cm_array):
        if cm > homog_field_left:
            homog_field_indexes.append(i)
            break
    for i, cm in enumerate(cm_array):
        if cm > homog_field_right:
            homog_field_indexes.append(i - 1)
            break
    homog_percent_array = sym_percent_array = percent_array[homog_field_indexes[0]:homog_field_indexes[1]]
    homog_max, homog_min = max(homog_percent_array), min(homog_percent_array)
    homog = homog_max - homog_min
    print(f"Homog. : {homog:.2f} %")

    sym_middle_index = int(len(sym_percent_array)/2)
    s_p_a_left = sym_percent_array[:sym_middle_index]
    s_p_a_right = sym_percent_array[sym_middle_index:]
    if len(s_p_a_left) < len(s_p_a_right):
        s_p_a_left = np.append(s_p_a_left, s_p_a_right[0])
    if len(s_p_a_left) > len(s_p_a_right):
        s_p_a_right = np.append(s_p_a_right, s_p_a_left[0])
    sym_deviation = max(abs(np.array(s_p_a_left) - np.array(s_p_a_right)[::-1]))
    print(f"Sym. : {sym_deviation:.2f} %")

    cm_array = cm_array - 9.7
    plt.scatter(cm_array, percent_array, color=color_list[index], s=1, label=curve_names[index])

plt.legend()
plt.xlabel("Distance avec l'isocentre (cm)")
plt.ylabel(r'Dose normalisée (D/D$_{max}$)')
plt.ylim(bottom=0)
plt.show()
