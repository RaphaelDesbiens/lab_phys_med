import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, normalize_slanted_field_profile, apply_ppwt_factor, read_roi
from a_etalonnage import od_to_dose
from fit_functions import gaussian_fit, gaussian_function

file_names = ["e) 0", "e) 30", "e) 60", "e) 90", "e) 120", "e) 150"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

# offset_od_parameter = 0.29
# offset_pixel_parameter = 250
# top_cm_parameter = 3.5
# slanted_mean_range = 60
go_smooth = True
smooth_range = 25
cut_range = int((smooth_range - 1)/2)
# low_percent_pen_list = [30, 30, 35, 35]
# high_percent_pen_list =[80, 80, 80, 80]

differences = []
for file_name in file_names:
    raw_pixel_list, raw_gray_list = read_profil(file_name)
    roi_pixel_list = read_roi(file_name)

    if go_smooth:
        raw_gray_list = smooth(raw_gray_list, smooth_range)
        raw_pixel_list = raw_pixel_list[cut_range:-cut_range]
        roi_pixel_list = [i - cut_range for i in roi_pixel_list]

    roi_gauss = roi_pixel_list[:2]
    roi_vert = roi_pixel_list[2:]

    pixel_list = raw_pixel_list[:roi_vert[0]] + raw_pixel_list[roi_vert[1]:]
    gray_list = raw_gray_list[:roi_vert[0]] + raw_gray_list[roi_vert[1]:]

    cut_pixel_list = pixel_list[roi_gauss[0]:roi_gauss[1]]
    cut_gray_list = gray_list[roi_gauss[0]:roi_gauss[1]]

    # a, mu, sigma, b
    a_approx = (gray_list[roi_vert[0]] - gray_list[roi_gauss[0]])*4
    mu_approx = (roi_gauss[0] + roi_gauss[1])/2
    sigma_approx = abs(roi_gauss[1] - roi_gauss[0])/2
    b_approx = gray_list[roi_gauss[0]]*2.5
    guesses = [a_approx, mu_approx, sigma_approx, b_approx]

    params, covariance = gaussian_fit(cut_pixel_list, cut_gray_list, guesses)
    a, mu, sigma, b = params[0], params[1], params[2], params[3]
    vert_gray_value = max(raw_gray_list[roi_vert[0]:roi_vert[1]])
    vert_index = raw_gray_list.index(vert_gray_value)
    vert_position = raw_pixel_list[vert_index]

    pixel_difference = abs(vert_position - mu)
    cm_difference = pixel_difference/118.5
    print(cm_difference)
    differences.append(cm_difference)
    # y_gauss = gaussian_function(cut_pixel_list, a, mu, sigma, b)
    # plt.plot(cut_pixel_list, y_gauss, linewidth=1, color=color_list[0])
    # plt.scatter(raw_pixel_list, raw_gray_list, s=1, color=color_list[1])
    # plt.show()

    # plt.plot(pixel_list, gray_list)
    # plt.scatter(full_pixel_list, rough_gray_list, s=1)

    # od_list = gray_to_od(gray_list)
    # od_profiles.append([pixel_list, od_list])

# field_size_list = []
# penumbra_list = []

# for index, od_profil in enumerate(od_profiles):
    # pixel_list = od_profil[0]
    # od_list = od_profil[1]
    # plt.scatter(raw_pixel_list, od_list, color=color_list[index], s=1, label=file_names[index][-2:])
    # for i, od in enumerate(od_list):
        # if od > offset_od_parameter:
            # offset = offset_pixel_parameter - i
            # pixel_list = [pixel + offset for pixel in raw_pixel_list]
            # break
    # cm_array = -apply_ppwt_factor(pixel_to_cm(pixel_list)) + 22.1346
    # dose_array = od_to_dose(od_list)
    # plt.scatter(cm_array, dose_array, color=color_list[index], s=1, label=file_names[index][-2:])

    # percent_array = normalize_slanted_field_profile(dose_array, slanted_mean_range)
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

    # plt.scatter(cm_array, percent_array, color=color_list[index], s=1, label=file_names[index][-2:])

# for y in [30, 35, 40, 45, 50]:
#     plt.plot([0, 21],[y, y])
# plt.legend(loc='upper right')
# plt.xlim(right=pixel_to_cm([2500]))
# plt.ylim(bottom=0)
# plt.show()