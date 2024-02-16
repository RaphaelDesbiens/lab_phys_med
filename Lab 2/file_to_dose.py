import matplotlib.pyplot as plt
import numpy as np
from profil_functions import read_profil, read_roi, cut_replace, smooth, gray_to_od, read_roi_inch, linear_calibration
from lab2_control import control_calibration
from lab2_0_etalonnage import calibrate


def file_to_dose(file_name, problems, smooth_range=None, is_open_profile=True, numero_3=False, numero_4=False):
    inch_list, gray_list = read_profil(file_name, distance='Distance_(inches)')
    roi = read_roi_inch(file_name)
    inch_array, gray_array = np.array(inch_list), np.array(gray_list)
    gray_array = cut_replace(inch_array, gray_array, problems)
    start, end = roi[0], roi[1]
    if numero_3:
        end = end + 32
    if numero_4:
        end = end + 15
    inch_array, gray_array = inch_array[start:end], gray_array[start:end]
    if smooth_range is not None:
        cut_range = int((smooth_range - 1) / 2)
        gray_array = smooth(gray_array, smooth_range)
        inch_array = inch_array[cut_range:-cut_range]
    gray_array = control_calibration(inch_array, gray_array)
    if is_open_profile:
        gray_array = linear_calibration(inch_array, gray_array)
    od_array = gray_to_od(gray_array)
    dose_array = calibrate(od_array)
    cm_array = np.array(inch_array)*2.54

    return cm_array, dose_array/2
