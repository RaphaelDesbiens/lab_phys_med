from profil_functions import read_profil, read_roi, cut_replace, smooth, gray_to_od
from lab2_control import control_calibration
from lab2_0_etalonnage import calibrate


def file_to_dose(file_name, extremities, smooth_range=None):
    inch_list, gray_list = read_profil(file_name)
    roi = read_roi(file_name)
    gray_list = cut_replace(inch_list, gray_list, extremities)
    start, end = roi[0], roi[1]
    inch_list, gray_list = inch_list[start:end], gray_list[start:end]
    if smooth_range is not None:
        cut_range = int((smooth_range - 1) / 2)
        gray_list = smooth(gray_list, smooth_range)
        inch_list = inch_list[cut_range:-cut_range]
    gray_list = control_calibration(inch_list, gray_list)
    od_array = gray_to_od(gray_list)
    dose_array = calibrate(od_array)

    return dose_array
