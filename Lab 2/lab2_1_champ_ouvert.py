import matplotlib.pyplot as plt
from file_to_dose import file_to_dose
from profil_functions import recenter_open_profile, normalize_open_profile

file_names = ["1am", "1a4", "1am2", "1a7"]
problems_list = [
                 [[2264, 2267], [2450, 2452]],
                 [[2028, 2030]],
                 [[2152, 2155]],
                 [[2100, 2102]]
                ]
smooth_range = None         # None for no smoothing

file_names_b = "1bm"
problems_list_b = [[2144, 2147]]
smooth_range_b = None         # None for no smoothing

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA']

for i, file_name in enumerate(file_names):
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range)
    cm_array = recenter_open_profile(cm_array, dose_array)
    percent_array = normalize_open_profile(dose_array)
    # plt.scatter(cm_array, dose_array, s=0.7, label=file_name)
    plt.scatter(cm_array, percent_array, s=0.7, label=file_name)

plt.legend()
plt.show()

