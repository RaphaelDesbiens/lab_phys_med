from file_to_dose import file_to_dose
from profil_functions import normalize_slanted_field_profile, read_profile_diode
import matplotlib.pyplot as plt

file_names = ["39", "39c", "315", "315c"]
problems_list = [
                 [[2172, 2174], [2358, 2359]],
                 [[2172, 2174], [2358, 2359]],
                 [[2100, 2103], [2286, 2287]],
                 []
                ]
smooth_range = None
slanted_mean_range = 50

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA']

cm_arrays_list, percent_arrays_list = [], []
for i, file_name in enumerate(file_names):
    print(f"--- {file_name} ---")
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range, is_open_profile=False, numero_3=True)
    cm_array = max(cm_array) - cm_array
    percent_array, top_dose = normalize_slanted_field_profile(dose_array, slanted_mean_range)
    # plt.scatter(cm_array, percent_array, s=0.3, label=file_name, color=color_list[i])

    cm_arrays_list.append(cm_array)
    percent_arrays_list.append(percent_array)

    r_50 = None
    for i, element in enumerate(percent_array):
        if element >= 50:
            r_50 = cm_array[i]
            print(f"R50 = {r_50:.2f}")
            break
    for i, element in enumerate(percent_array):
        if element >= 80:
            r_80 = cm_array[i]
            print(f"R80 = {r_80:.2f}")
            break
    for i, element in enumerate(percent_array):
        if element >= 90:
            r_90 = cm_array[i]
            print(f"R90 = {r_90:.2f}")
            break
    r_p = 1.271*r_50 - 0.23
    print(f"R_p = {r_p:.2f}")
    e_p0 = 0.22 + 1.98*r_p + 0.0025*r_p**2
    print(f"E_p0 = {e_p0:.2f}")
    e_0 = 0.656 + 2.059*r_50 + 0.022*r_50**2
    print(f"E_0 = {e_0:.2f}")
    print("\n")

for i, file_name in enumerate(file_names):
    print(f"--- diode_{file_name} ---")
    cm_array, percent_array, current_array = read_profile_diode(file_name, x_column=2)
    # plt.scatter(cm_array, percent_array, s=8, color=color_list[i], label=file_name + " - diode",
    #             marker='^')

    cm_arrays_list.append(cm_array)
    percent_arrays_list.append(percent_array)

    r_50 = None
    for i, element in enumerate(percent_array):
        if element >= 50:
            r_50 = cm_array[i]
            print(f"R50 = {r_50:.2f}")
            break
    for i, element in enumerate(percent_array):
        if element >= 80:
            r_80 = cm_array[i]
            print(f"R80 = {r_80:.2f}")
            break
    for i, element in enumerate(percent_array):
        if element >= 90:
            r_90 = cm_array[i]
            print(f"R90 = {r_90:.2f}")
            break
    r_p = 1.271 * r_50 - 0.23
    print(f"R_p = {r_p:.2f}")
    e_p0 = 0.22 + 1.98 * r_p + 0.0025 * r_p ** 2
    print(f"E_p0 = {e_p0:.2f}")
    e_0 = 0.656 + 2.059 * r_50 + 0.022 * r_50 ** 2
    print(f"E_0 = {e_0:.2f}")
    print("\n")


def get_3_arrays():

    return cm_arrays_list, percent_arrays_list


if __name__ == "__main__":
    plt.xlim(0)
    plt.ylim(-5, 110)
    plt.legend()
    plt.show()