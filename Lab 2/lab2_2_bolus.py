import matplotlib.pyplot as plt
from file_to_dose import file_to_dose
from profil_functions import recenter_open_profile, normalize_slanted_field_profile, measure_field_size, \
    measure_penumbra

file_names = ["2m", "24"]
problems_list = [
                 [[2009, 2011]],
                 [[2288, 2291], [2474, 2476]]
                ]
smooth_range = 5

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA']

cm_arrays_list, percent_arrays_list = [], []
for i, file_name in enumerate(file_names):
    cm_array, dose_array = file_to_dose(file_name, problems_list[i], smooth_range)
    cm_array = recenter_open_profile(cm_array, dose_array)
    if file_name == "24":
        cm_array = cm_array - 3
    else:
        cm_array = cm_array - 0.55
    percent_array, top_dose = normalize_slanted_field_profile(dose_array, 80)

    # plt.scatter(cm_array, dose_array, s=0.7, label=file_name)
    # plt.scatter(cm_array, percent_array, s=0.7, label=file_name)
    if file_name == "24":
        percent_array = 100*dose_array / 1.97

    cm_arrays_list.append(cm_array)
    percent_arrays_list.append(percent_array)

    field_edges = measure_field_size(cm_array, percent_array)
    # field_size = field_edges[1] - field_edges[0]
    # print(f"field_size = {field_size:.2f}")

    # left_penumbra, right_penumbra = measure_penumbra(cm_array, percent_array, [20, 80])
    # print(f"penumbras = [{left_penumbra:.2f}, {right_penumbra:.2f}]")


def get_2_arrays():

    return cm_arrays_list, percent_arrays_list


if __name__ == "__main__":
    plt.legend()
    plt.show()