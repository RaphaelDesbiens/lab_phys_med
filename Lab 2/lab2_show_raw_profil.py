import matplotlib.pyplot as plt
import numpy as np
import os
from profil_functions import read_profil, read_profile_diode
import pandas as pd

etalonnage_file_names = ['etalonnage_0.5Gy',
 'etalonnage_0.25Gy',
 'etalonnage_0Gy',
 'etalonnage_1.5Gy',
 'etalonnage_1Gy',
 'etalonnage_2Gy',
 'etalonnage_3Gy',
 'etalonnage_4Gy',
 'etalonnage_5Gy']

file_names = ["1am", "1a4", "1am2", "1a7", "1bm", "2m", "24", "39", "39c", "315", "315c", "40", "4m", "5s", "515"]

diode_file_names = ["1am", "1am2", "1bm"]

rp_diode_file_names = ["39", "39c", "315", "315c"]

control_file_names = ["controle", "controle_blanc_1", "controle_blanc_2"]

color_list = [
    u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080', u'#00FFFF', u'#FF00FF', u'#808000',
    u'#800000', u'#008080', u'#000080', u'#808080', u'#FFFF00', u'#00FF00', u'#FFC0CB', u'#FFD700',
    u'#FF4500', u'#DA70D6', u'#EEE8AA', u'#FA8072', u'#FDF5E6', u'#FFDAB9', u'#FFA07A', u'#D2691E',
    u'#CD853F', u'#F4A460', u'#8B4513', u'#A0522D', u'#A52A2A', u'#800000', u'#FFFFFF', u'#F5F5F5',
    u'#DCDCDC', u'#D3D3D3', u'#C0C0C0', u'#A9A9A9', u'#808080', u'#696969', u'#000000', u'#2F4F4F',
    u'#708090', u'#778899', u'#B0C4DE', u'#E6E6FA', u'#FFFAFA', u'#F0F8FF', u'#F8F8FF', u'#F0FFF0',
    u'#FFFFF0', u'#F0FFFF', u'#FFFAF0', u'#FFF5EE', u'#F5FFFA', u'#FFF0F5', u'#FAEBD7', u'#FAF0E6',
    u'#FFF8DC', u'#FFFFE0', u'#8A2BE2', u'#A52A2A', u'#DEB887', u'#5F9EA0', u'#7FFF00', u'#D2691E',
    u'#FF7F50', u'#6495ED', u'#FFF8DC', u'#DC143C', u'#00FFFF', u'#00008B', u'#008B8B', u'#B8860B',
    u'#A9A9A9', u'#006400', u'#BDB76B', u'#8B008B', u'#556B2F', u'#FF8C00', u'#9932CC', u'#8B0000',
    u'#E9967A', u'#8FBC8F', u'#483D8B', u'#2F4F4F', u'#00CED1', u'#9400D3', u'#FF1493', u'#00BFFF',
    u'#696969', u'#1E90FF', u'#B22222', u'#FFFAF0', u'#228B22', u'#FF00FF', u'#DCDCDC', u'#F8F8FF',
    u'#FFD700', u'#DAA520', u'#808080', u'#008000', u'#ADFF2F', u'#F0FFF0', u'#FF69B4', u'#CD5C5C',
    u'#4B0082', u'#FFFFF0', u'#F0E68C', u'#E6E6FA', u'#FFF0F5', u'#7CFC00', u'#FFFACD', u'#ADD8E6',
    u'#F08080', u'#E0FFFF', u'#FAFAD2', u'#D3D3D3', u'#90EE90', u'#D3D3D3', u'#FFB6C1', u'#FFA07A',
    u'#20B2AA', u'#87CEFA', u'#778899', u'#B0C4DE', u'#FFFFE0', u'#00FF00', u'#32CD32', u'#FAF0E6',
    u'#FF00FF', u'#800000', u'#66CDAA', u'#0000CD', u'#BA55D3', u'#9370DB', u'#3CB371', u'#7B68EE',
    u'#00FA9A', u'#48D1CC', u'#C71585', u'#191970', u'#F5FFFA', u'#FFE4E1'
    ]

for i, file_name in enumerate(etalonnage_file_names):
    raw_pixel_list, raw_gray_list = read_profil(file_name)
    # plt.scatter(raw_pixel_list, raw_gray_list, s=0.5, color=color_list[i])

for i, file_name in enumerate(file_names[-2:]):
    raw_pixel_list, raw_gray_list = read_profil(file_name, distance='Distance_(inches)')
    plt.scatter(raw_pixel_list, raw_gray_list, s=1.5, color=color_list[i], label=file_name)
    # plt.legend()
    # plt.show()

for i, file_name in enumerate(["39", "39c", "315", "315c"]):
    raw_pixel_list, raw_gray_list = read_profil(file_name, distance='Distance_(inches)')
    # plt.scatter(raw_pixel_list, raw_gray_list, s=1.5, color=color_list[i], label=file_name)
    # plt.legend()

for i, file_name in enumerate(["1am", "1a4", "1am2", "1a7"]):
    raw_pixel_list, raw_gray_list = read_profil(file_name, distance='Distance_(inches)')
    # plt.scatter(raw_pixel_list, raw_gray_list, s=1.5, color=color_list[i], label=file_name)

for i, file_name in enumerate(control_file_names):
    raw_pixel_list, raw_gray_list = read_profil(file_name, distance='Distance_(inches)')
    if file_name == "controle":
        raw_gray_list = np.array(raw_gray_list) + 12500
    # plt.scatter(raw_pixel_list, raw_gray_list, s=0.8, color=color_list[i], label=file_name)
    # plt.legend()
    # plt.show()

for i, file_name in enumerate(diode_file_names):
    mm_array, percent_array = read_profile_diode(file_name)
    # plt.scatter(mm_array, percent_array, s=1.5, color=color_list[i], label=file_name)

for i, file_name in enumerate(rp_diode_file_names):
    mm_array, percent_array = read_profile_diode(file_name, x_column=2)
    # plt.scatter(mm_array, percent_array, s=1.5, color=color_list[i], label=file_name)

plt.legend()
plt.show()
