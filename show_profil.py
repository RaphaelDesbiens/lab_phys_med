import matplotlib.pyplot as plt
from profil_functions import read_profil, gray_to_od, pixel_to_cm, normalize_field_profile, \
    measure_field_size, measure_penumbra, smooth, normalize_slanted_field_profile, apply_ppwt_factor, read_roi
from a_etalonnage import od_to_dose
from fit_functions import gaussian_fit, gaussian_function

li = [12,34,5,7,6,1,6]
print(li[2:-1])

#file_name = "e) 60"

#raw_pixel_list, raw_gray_list = read_profil(file_name)
#roi_pixel_list = read_roi(file_name)
#print(roi_pixel_list)

#plt.scatter(raw_pixel_list, raw_gray_list)
#plt.show()