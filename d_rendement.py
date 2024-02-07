import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, normalize_slanted_field_profile, apply_ppwt_factor
from a_etalonnage import od_to_dose
import statistics as stat

file_names = ["d) rendement"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

# offset_od_parameter = 0.29
# offset_pixel_parameter = 250
# top_cm_parameter = 3.5
go_smooth = False
smooth_range = 35
cut_range = int((smooth_range - 1)/2)
slanted_mean_range = 60

# low_percent_pen_list = [30, 30, 35, 35]
# high_percent_pen_list =[80, 80, 80, 80]

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

# field_size_list = []
# penumbra_list = []

for index, od_profil in enumerate(od_profiles):
    pixel_list = od_profil[0]
    od_list = od_profil[1]
    # plt.scatter(raw_pixel_list, od_list, color=color_list[index], s=1, label=file_names[index][-2:])
    # for i, od in enumerate(od_list):
        # if od > offset_od_parameter:
            # offset = offset_pixel_parameter - i
            # pixel_list = [pixel + offset for pixel in raw_pixel_list]
            # break
    cm_array = -apply_ppwt_factor(pixel_to_cm(pixel_list)) + 22.1346
    dose_array = od_to_dose(od_list)
    # plt.scatter(cm_array, dose_array, color=color_list[index], s=1, label=file_names[index][-2:])

    percent_array = normalize_slanted_field_profile(dose_array, slanted_mean_range)
    # if file_names[index][-1] == "x":
        # range_100 = []
        # for ind, cm in enumerate(cm_array):
            # if cm >= top_cm_parameter:
                # range_100.append(ind)
                # break
        # range_100.append(range_100[0] + 1120)
        # percent_array = normalize_field_profile(dose_array, range_100)
    # else:
        # percent_array = normalize_slanted_field_profile(dose_array, slanted_mean_range)

    plt.scatter(cm_array, percent_array, color=color_list[index], s=1, label=file_names[index][-2:])

# for y in [30, 35, 40, 45, 50]:
#     plt.plot([0, 21],[y, y])
plt.legend(loc='upper right')
# plt.xlim(right=pixel_to_cm([2500]))
plt.ylim(bottom=0)
plt.show()