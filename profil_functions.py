import pandas as pd
import os
import statistics as stat
import numpy as np


def read_profil(file_name):
    file_path = os.path.join(r".\csv_files", file_name + ".csv")
    df = pd.read_csv(file_path)
    pixel_list = df['Distance_(pixels)'].tolist()
    gray_list = df['Gray_Value'].tolist()

    return pixel_list, gray_list


def read_roi(file_name):
    roi_file_path = os.path.join(r".\csv_files", file_name + "_ROI.csv")
    roi_df = pd.read_csv(roi_file_path)
    roi_pixel_list = [int(pixel) for pixel in roi_df['X'].tolist()]

    return roi_pixel_list


def gray_to_od(gray_values_list, white_value=65535):
    optical_density = np.log10(white_value / np.array(gray_values_list))

    return optical_density


def pixel_to_cm(pixel_list):
    inch_array = np.array(pixel_list)/300
    cm_array = inch_array*2.54

    return cm_array


def apply_ppwt_factor(x_array):

    return x_array*1.286 - 0.6


def normalize_field_profile(dose_array, range_100):
    start = range_100[0]
    end = range_100[1]
    top = stat.mean(dose_array[start:end])

    return 100*dose_array/top


def normalize_slanted_field_profile(dose_array, slanted_mean_range):
    top_dose = 0
    for element in range(len(dose_array) + 1 - slanted_mean_range):
        slanted_mean = stat.mean(dose_array[element:element + slanted_mean_range])
        if slanted_mean > top_dose:
            top_dose = slanted_mean

    return 100*dose_array/top_dose

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

    return smoothed_list
