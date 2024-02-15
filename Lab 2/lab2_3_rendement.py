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

for i, file_name in enumerate(file_names):
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range, is_open_profile=False)
    cm_array = max(cm_array) - cm_array
    percent_array, top_dose = normalize_slanted_field_profile(dose_array, slanted_mean_range)
    plt.scatter(cm_array, percent_array, s=0.3, label=file_name, color=color_list[i])

for i, file_name in enumerate(file_names):
    cm_array, percent_array, current_array = read_profile_diode(file_name, x_column=2)
    plt.scatter(cm_array, percent_array, s=8, color=color_list[i], label=file_name + " - diode",
                marker='^')

plt.legend()
plt.show()
