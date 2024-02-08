import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, apply_ppwt_factor
from a_etalonnage import od_to_dose
import statistics as stat

file_names = ["b) 1x", "b) 1y", "b) 2x", "b) 2y"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

offset_od_parameter = 0.33
offset_pixel_parameter = 250
top_cm_parameter = 3.5
go_smooth = True
smooth_range = 5
cut_range = int((smooth_range - 1)/2)

low_percent_pen_list = [30, 30, 35, 35]
high_percent_pen_list =[80, 80, 80, 80]

od_profiles = []
for file_name in file_names:
    pixel_list, gray_list = read_profil(file_name)
    full_pixel_list = pixel_list
    rough_gray_list = gray_list
    if go_smooth:
        gray_list = smooth(rough_gray_list, smooth_range)
        pixel_list = full_pixel_list[cut_range:-cut_range]

    # plt.plot(pixel_list, gray_list)
    # plt.scatter(full_pixel_list, rough_gray_list, s=1)

    od_list = gray_to_od(gray_list)
    od_profiles.append([pixel_list, od_list])

field_size_list = []
penumbra_list = []

for index, od_profil in enumerate(od_profiles):
    raw_pixel_list = od_profil[0]
    od_list = od_profil[1]
    pixel_list = []
    # plt.scatter(raw_pixel_list, od_list, color=color_list[index], s=1, label=file_names[index][-2:])
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

    percent_array = normalize_field_profile(dose_array, range_100)

    # if file_names[index][-2:] == "2y" or file_names[index][-2:] == "1x":
    #     cm_array = cm_array*1.286 - 0.6

    plt.scatter(cm_array, percent_array, color=color_list[index], s=1, label=file_names[index][-2:])

    field_edges = measure_field_size(cm_array, percent_array)
    field_size = field_edges[1] - field_edges[0]
    field_size_list.append(field_size)

    low_percent_pen = low_percent_pen_list[index]
    high_percent_pen = high_percent_pen_list[index]
    left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [low_percent_pen, high_percent_pen])
    penumbra_list.append([left_penumbra, right_penumbra])

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

    sym_field_indexes = homog_field_indexes
    sym_middle_index = int(stat.mean(sym_field_indexes))
    sym_average_percent_left = stat.mean(sym_percent_array[sym_field_indexes[0]:sym_middle_index])
    sym_average_percent_right = stat.mean(sym_percent_array[sym_middle_index:sym_field_indexes[1]])
    sym_deviations = [100*abs(sym_average_percent_left - sym_average_percent_right) / sym_average_percent_left,
                  100*abs(sym_average_percent_left - sym_average_percent_right) / sym_average_percent_right]
    sym_deviation = max(sym_deviations)
    print(f"Sym. : {sym_deviation:.2f} %")

# plt.plot([0, 20],[30, 30])
# plt.plot([0, 20],[60, 60], linewidth=0.1)
plt.legend(loc='upper right')
plt.xlim(right=pixel_to_cm([2500]))
plt.ylim(bottom=0)
plt.show()
