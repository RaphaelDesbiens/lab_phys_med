import matplotlib.pyplot as plt
from file_to_dose import file_to_dose
from profil_functions import recenter_open_profile, normalize_open_profile, read_profile_diode, measure_field_size, \
    measure_penumbra, measure_homog_and_sym
import pandas as pd

file_names = ["1am", "1a4", "1am2", "1a7"]
problems_list = [
                 [[2264, 2267], [2450, 2452]],
                 [[2028, 2030]],
                 [[2152, 2155]],
                 [[2100, 2102]]
                ]
smooth_range = 9         # None for no smoothing

file_names_b = ["1bm"]
problems_b = [[2144, 2147]]
smooth_range_b = None         # None for no smoothing

diode_file_names = ["1am", "1am2", "1bm"]
color_equivalent = [0, 2, 4]

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA']

dose = None
for i, file_name in enumerate(file_names):
    print(f"--- {file_name} ---")
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range)
    cm_array = recenter_open_profile(cm_array, dose_array)
    plt.scatter(cm_array, dose_array, s=0.7, label=file_name, color=color_list[i])
    percent_array, top_dose = normalize_open_profile(dose_array)
    print(f"top_dose = {top_dose:.2f} Gy")
    # plt.scatter(cm_array, percent_array, s=0.7, label=file_name, color=color_list[i])
    if file_name in ["1am", "1am2"]:
        dose = top_dose
    if file_name in ["1a4", "1a7"]:
        pdd = 100*top_dose/dose
        print(f"PDD = {pdd:.2f} %")


    field_edges = measure_field_size(cm_array, percent_array)
    field_size = field_edges[1] - field_edges[0]
    print(f"field_size = {field_size:.2f}")

    left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [20, 80])
    print(f"penumbras = [{left_penumbra:.2f} - {right_penumbra:.2f}]")

    homog, sym_deviation = measure_homog_and_sym(cm_array, percent_array, field_edges)
    print(f"Homog. : {homog:.2f} %")
    print(f"Sym. : {sym_deviation:.2f} %\n")

for i, file_name in enumerate(file_names_b):
    print(f"--- {file_name} ---")
    cm_array, dose_array = file_to_dose(file_name, problems_b, smooth_range_b)
    cm_array = recenter_open_profile(cm_array, dose_array)
    plt.scatter(cm_array, dose_array, s=0.7, label=file_name, color=color_list[4])
    percent_array, top_dose = normalize_open_profile(dose_array)
    print(f"top_dose = {top_dose:.2f} Gy")
    # plt.scatter(cm_array, percent_array, s=0.7, label=file_name, color=color_list[4])

    field_edges = measure_field_size(cm_array, percent_array)
    field_size = field_edges[1] - field_edges[0]
    print(f"field_size = {field_size:.2f}")

    left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [20, 80])
    print(f"penumbras = [{left_penumbra:.2f} - {right_penumbra:.2f}]")

    homog, sym_deviation = measure_homog_and_sym(cm_array, percent_array, field_edges)
    print(f"Homog. : {homog:.2f} %")
    print(f"Sym. : {sym_deviation:.2f} %\n")

for i, file_name in enumerate(diode_file_names):
    print(f"--- diode_{file_name} ---")
    cm_array, percent_array, current_array = read_profile_diode(file_name)
    cm_array = -cm_array
    # plt.scatter(cm_array, current_array, s=3, color=color_list[color_equivalent[i]], label=file_name + " - diode",
    #             marker='^')
    # plt.scatter(cm_array, percent_array, s=3, color=color_list[color_equivalent[i]], label=file_name + " - diode",
    #             marker='^')

    field_edges = measure_field_size(cm_array, percent_array)
    field_size = field_edges[1] - field_edges[0]
    print(f"field_size = {field_size:.2f}")

    left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [20, 80])
    print(f"penumbras = [{left_penumbra:.2f}, {right_penumbra:.2f}]")

    homog, sym_deviation = measure_homog_and_sym(cm_array, percent_array, field_edges)
    print(f"Homog. : {homog:.2f} %")
    print(f"Sym. : {sym_deviation:.2f} %\n")

plt.legend()
plt.show()

