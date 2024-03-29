import pandas as pd
import os
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt


def read_profil(file_name, distance='Distance_(pixels)', y_name='Gray_Value'):
    file_path = os.path.join(r".\csv_files", file_name + ".csv")
    df = pd.read_csv(file_path)
    pixel_list = df[distance].tolist()
    gray_list = df[y_name].tolist()

    return pixel_list, gray_list


def read_profile_diode(file_name, x_column=0, y_column_normalized=3, y_column_current=4):
    file_path = os.path.join(r".\csv_files", "diode_" + file_name + ".csv")
    df = pd.read_csv(file_path, sep=';', skiprows=18)
    mm_array = df.iloc[:, x_column].to_numpy()
    cm_array = mm_array/10
    percent_array = df.iloc[:, y_column_normalized].to_numpy()
    current_array = df.iloc[:, y_column_current].to_numpy()

    return cm_array, percent_array, current_array


def read_roi(file_name):
    roi_file_path = os.path.join(r".\csv_files", file_name + "_ROI.csv")
    roi_df = pd.read_csv(roi_file_path)
    roi_pixel_list = [int(pixel) for pixel in roi_df['X'].tolist()]

    return roi_pixel_list


def read_roi_inch(file_name):
    roi_file_path = os.path.join(r".\csv_files", file_name + "_ROI.csv")
    roi_df = pd.read_csv(roi_file_path)
    roi_pixel_list = [int(inch*300) for inch in roi_df['X'].tolist()]

    return roi_pixel_list


def gray_to_od(gray_values_list, white_value=65535):
    optical_density = np.log10(white_value / np.array(gray_values_list))

    return optical_density


def pixel_to_cm(pixel_list):
    inch_array = np.array(pixel_list)/300
    cm_array = inch_array*2.54

    return cm_array


def apply_ppwt_factor(x_array):
    """
    Puisque j'obtenais des valeurs de gris inconsistentes d'une fois à l'autre que je faisais mes profils sur
    imageJ, j'ai pris tous les scans et je les ai groupé en une image pour pouvoir faire tous mes profils en une seule
    batch. Le fait de les grouper a changé la résolution, d'où le facteur suivant.
    """
    return x_array*1.286 - 0.6


def normalize_field_profile(dose_array, range_100):
    start = range_100[0]
    end = range_100[1]
    top_dose = stat.mean(dose_array[start:end])

    return 100*dose_array/top_dose, top_dose


def normalize_slanted_field_profile(dose_array, slanted_mean_range):
    top_dose = 0
    for element in range(len(dose_array) + 1 - slanted_mean_range):
        slanted_mean = stat.mean(dose_array[element:element + slanted_mean_range])
        if slanted_mean > top_dose:
            top_dose = slanted_mean

    return 100*dose_array/top_dose, top_dose


def measure_field_size(cm_array, percent_array):
    field_dimensions = []
    for index, percent in enumerate(percent_array):
        if percent >= 50:
            field_dimensions.append(cm_array[index])
            break
    for index, percent in enumerate(reversed(percent_array)):
        if percent >= 50:
            original_index = len(percent_array) - 1 - index
            field_dimensions.append(cm_array[original_index])
            break

    return field_dimensions


def measure_penumbra(cm_array, percent_array, percent_range):
    penumbra_dimensions = [[], []]
    low_percent, high_percent = percent_range[0], percent_range[1]
    first, second = True, False
    for index, percent in enumerate(percent_array):
        if (percent >= low_percent) and first:
            penumbra_dimensions[0].append(cm_array[index])
            first, second = False, True
        if (percent > high_percent) and second:
            penumbra_dimensions[0].append(cm_array[index - 1])
            first, second = True, False
            break
    for index, percent in enumerate(reversed(percent_array)):
        if (percent >= low_percent) and first:
            original_index = len(percent_array) - 1 - index
            penumbra_dimensions[1].append(cm_array[original_index])
            first, second = False, True
        if (percent > high_percent) and second:
            original_index = len(percent_array) - 1 - index
            penumbra_dimensions[1].insert(0, cm_array[original_index - 1])
            break

    left = penumbra_dimensions[0][1] - penumbra_dimensions[0][0]
    right = penumbra_dimensions[1][1] - penumbra_dimensions[1][0]

    return left, right


def smooth(gray_list, mean_range):
    smoothed_list = []
    for element in range(len(gray_list) + 1 - mean_range):
        smoothed_list.append(stat.mean(gray_list[element:element + mean_range]))

    return np.array(smoothed_list)


def cut_replace(x_array, y_array, problems, buffer=20):
    new_y_array = y_array
    for extremities in problems:
        start, end = extremities[0], extremities[1] + 1
        x1, y1 = x_array[int(start - buffer/2)], stat.mean(y_array[start - 1 - buffer:start - 1])
        x2, y2 = x_array[int(end + buffer/2)], stat.mean(y_array[end + 1:end + 1 + buffer])
        m = (y2 - y1)/(x2 - x1)
        b = y1 - m*x1
        y_piece = m*x_array[start:end] + b
        new_y_array = np.array(new_y_array[:start].tolist() + y_piece.tolist() + new_y_array[end:].tolist())

    return new_y_array


def recenter_open_profile(x_array, y_array):
    field_edges = []        # cm
    middle_y_value = (min(y_array) + max(y_array))/2
    for i, y_value in enumerate(y_array):
        if y_value >= middle_y_value:
            field_edges.append(x_array[i])
            break
    for i, y_value in enumerate(reversed(y_array)):
        if y_value >= middle_y_value:
            original_index = len(y_array) - 1 - i
            field_edges.append(x_array[original_index])
            break

    return x_array - stat.mean(field_edges)


def normalize_open_profile(y_array):
    field_edges = []        # index
    threshold_y_value = 0.8*max(y_array)
    for i, y_value in enumerate(y_array):
        if y_value >= threshold_y_value:
            field_edges.append(i)
            break
    for i, y_value in enumerate(reversed(y_array)):
        if y_value >= threshold_y_value:
            original_index = len(y_array) - 1 - i
            field_edges.append(original_index)
            break
    field_size = field_edges[1] - field_edges[0]
    left_edge = int(field_edges[0] + 0.15 * field_size)
    right_edge = int(field_edges[1] - 0.15 * field_size)
    top_value = stat.mean(y_array[left_edge:right_edge])
    percent_array = 100*y_array/top_value

    return percent_array, top_value


def linear_calibration(x_array, y_array):
    y1 = stat.mean(y_array[:50])
    y2 = stat.mean(y_array[-50:])
    x1 = x_array[25]
    x2 = x_array[-25]
    m = (y2 - y1)/(x2 - x1)
    new_y_array = y_array - m*(x_array-min(x_array))

    return new_y_array


def find_smoothed_max(y_list, mean_range):
    smoothed_max = 0
    for element in range(len(y_list) + 1 - mean_range):
        moving_mean = stat.mean(y_list[element:element + mean_range])
        if moving_mean > smoothed_max:
            smoothed_max = moving_mean

    return smoothed_max


def measure_homog_and_sym(cm_array, percent_array, field_edges):
    field_size = field_edges[1] - field_edges[0]
    homog_field_left = field_edges[0] + 0.1 * field_size
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
    homog = 100 + (homog_max - homog_min)/2

    sym_middle_index = int(len(sym_percent_array) / 2)
    s_p_a_left = sym_percent_array[:sym_middle_index]
    s_p_a_right = sym_percent_array[sym_middle_index:]
    if len(s_p_a_left) < len(s_p_a_right):
        s_p_a_left = np.append(s_p_a_left, s_p_a_right[0])
    if len(s_p_a_left) > len(s_p_a_right):
        s_p_a_right = np.append(s_p_a_right, s_p_a_left[0])
    sym_deviation = max(abs(np.array(s_p_a_left) - np.array(s_p_a_right)[::-1]))

    return homog, sym_deviation
