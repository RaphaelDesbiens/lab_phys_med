from file_to_dose import file_to_dose
from profil_functions import normalize_slanted_field_profile
import matplotlib.pyplot as plt

file_names = ["40", "4m"]
problems_list = [
                 [[2100, 2104]],
                 [[2100, 2102], [2286, 2287]]
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
    plt.scatter(cm_array, percent_array, s=0.7, label=file_name, color=color_list[i])

plt.show()
