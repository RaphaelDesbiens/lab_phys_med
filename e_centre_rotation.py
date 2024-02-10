from profil_functions import read_profil, smooth, read_roi
from fit_functions import gaussian_fit

file_names = ["e) 0", "e) 30", "e) 60", "e) 90", "e) 120", "e) 150"]

color_list = ['#FF0000', '#008000', '#0000FF', '#FFA500', '#800080', '#00FFFF', '#FF00FF']

go_smooth = True
smooth_range = 25
cut_range = int((smooth_range - 1)/2)

differences = []
for file_name in file_names:
    raw_pixel_list, raw_gray_list = read_profil(file_name)
    roi_pixel_list = read_roi(file_name)

    if go_smooth:
        raw_gray_list = smooth(raw_gray_list, smooth_range)
        raw_pixel_list = raw_pixel_list[cut_range:-cut_range]
        roi_pixel_list = [i - cut_range for i in roi_pixel_list]

    roi_gauss = roi_pixel_list[:2]
    roi_vert = roi_pixel_list[2:]

    pixel_list = raw_pixel_list[:roi_vert[0]] + raw_pixel_list[roi_vert[1]:]
    gray_list = raw_gray_list[:roi_vert[0]] + raw_gray_list[roi_vert[1]:]

    cut_pixel_list = pixel_list[roi_gauss[0]:roi_gauss[1]]
    cut_gray_list = gray_list[roi_gauss[0]:roi_gauss[1]]

    a_approx = (gray_list[roi_vert[0]] - gray_list[roi_gauss[0]])*4
    mu_approx = (roi_gauss[0] + roi_gauss[1])/2
    sigma_approx = abs(roi_gauss[1] - roi_gauss[0])/2
    b_approx = gray_list[roi_gauss[0]]*2.5
    guesses = [a_approx, mu_approx, sigma_approx, b_approx]

    params, covariance = gaussian_fit(cut_pixel_list, cut_gray_list, guesses)
    a, mu, sigma, b = params[0], params[1], params[2], params[3]
    vert_gray_value = max(raw_gray_list[roi_vert[0]:roi_vert[1]])
    vert_index = raw_gray_list.index(vert_gray_value)
    vert_position = raw_pixel_list[vert_index]

    pixel_difference = abs(vert_position - mu)
    cm_difference = pixel_difference/118.5
    print(cm_difference)
    differences.append(cm_difference)
