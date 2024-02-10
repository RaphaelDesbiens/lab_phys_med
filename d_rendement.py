import matplotlib.pyplot as plt
import numpy as np
from profil_functions import read_profil, gray_to_od, pixel_to_cm, smooth, normalize_slanted_field_profile, \
    apply_ppwt_factor
from a_etalonnage import od_to_dose
from fit_functions import pdd_fit, pdd_function, expon_fit, expon_function

file_names = ["d) rendement"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

go_smooth = False
smooth_range = 35
cut_range = int((smooth_range - 1)/2)
slanted_mean_range = 60

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
    pixel_list = od_profil[0]
    od_list = od_profil[1]
    offset_cm_array = -apply_ppwt_factor(pixel_to_cm(pixel_list)) + 22.1346
    hidden_cm = apply_ppwt_factor(pixel_to_cm([9]))[0] + 0.6
    cm_array = offset_cm_array - offset_cm_array[-1] + hidden_cm
    dose_array = od_to_dose(od_list)

    percent_array, top_doze = normalize_slanted_field_profile(dose_array, slanted_mean_range)
    expon_cutoff_index = int(14*len(cm_array)/20)
    cm_array_expon, percent_array_expon = cm_array[:expon_cutoff_index], percent_array[:expon_cutoff_index]
    params_expon, covariance_expon = expon_fit(cm_array_expon, percent_array_expon)
    a, mu = params_expon[0], params_expon[1]
    print(f"mu_exp = {mu}")
    print(f"a_exp = {a}")
    x_expon = np.linspace(10, 21, 10000)
    y_values_expon = expon_function(x_expon, a, mu) - 1.2
    plt.plot(x_expon, y_values_expon, color=color_list[2], linewidth=1, zorder=5)

    pdd_cutoff_index = int(14 * len(cm_array) / 20)
    cm_array_pdd, percent_array_pdd = cm_array[pdd_cutoff_index:], percent_array[pdd_cutoff_index:]
    params, covariance = pdd_fit(cm_array_pdd, percent_array_pdd, [75, -0.7, 0.04, 30])
    a_pdd, n, mu_pdd, b_pdd = params[0], params[1], params[2], params[3]
    print(f"a_pdd = {a_pdd}")
    print(f"n_pdd = {n}")
    print(f"mu_pdd = {mu_pdd}")
    print(f"b_pdd = {b_pdd}")
    x_values = np.linspace(0.05, 10, 10000)
    y_values = pdd_function(x_values, a_pdd, n, mu_pdd, b_pdd)
    max_y = max(y_values)
    max_index = y_values.tolist().index(max_y)
    d_max = x_values[max_index]
    print(f"d_max = {d_max:.2f} cm")
    d_100 = (pdd_function(10, a_pdd, n, mu_pdd, b_pdd) + expon_function(10, a, mu))/2
    d_200 = expon_function(20, a, mu)
    d_50 = pdd_function(5, a_pdd, n, mu_pdd, b_pdd)
    ratio_100_200 = d_100/d_200
    print(f"D100 = {d_100:.2f}")
    print(f"D200 = {d_200:.2f}")
    print(f"D50 = {d_50:.2f}")
    print(f"D100/D200 = {ratio_100_200:.2f}")

    plt.plot(x_values, y_values, color=color_list[2], label="Modélisation PDD", linewidth=1, zorder=5)

    plt.scatter(cm_array, percent_array, color=color_list[index], s=0.3, label="Données expérimentales", zorder=10)

plt.legend()
plt.xlabel("Profondeur (cm)")
plt.ylabel(r'Dose normalisée (D/D$_{max}$)')
plt.ylim(bottom=0)
plt.show()