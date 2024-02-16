from file_to_dose import file_to_dose
from profil_functions import recenter_open_profile, normalize_open_profile
import matplotlib.pyplot as plt

file_names = ["5s", "515"]
problems_list = [
                 [[2092, 2096]],
                 [[2216, 2219], [2402, 2404]]
                ]
smooth_range = None

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA']

cm_arrays_list, percent_arrays_list = [], []
for i, file_name in enumerate(file_names):
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range)
    cm_array = recenter_open_profile(cm_array, dose_array)
    # plt.scatter(cm_array, dose_array, s=0.7, label=file_name, color=color_list[i])
    percent_array, top_dose = normalize_open_profile(dose_array)
    # plt.scatter(cm_array, percent_array, s=0.7, label=file_name, color=color_list[i])

    if file_name == "5s":
        percent_array = 100*dose_array/1.7

    cm_arrays_list.append(cm_array)
    percent_arrays_list.append(percent_array)


def get_5_arrays():

    return cm_arrays_list, percent_arrays_list


if __name__ == "__main__":
    plt.legend()
    plt.show()
