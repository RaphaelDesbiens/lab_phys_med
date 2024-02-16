from lab2_1_champ_ouvert import get_1_arrays
from lab2_2_bolus import get_2_arrays
from lab2_3_rendement import get_3_arrays
from lab2_4_oblique import get_4_arrays
from lab2_5_jonction import get_5_arrays
import matplotlib.pyplot as plt

color_list = [u'#FF0000', u'#008000', u'#0000FF', u'#FFA500', u'#800080',
              u'#00FFFF', u'#FF00FF', u'#808000', u'#800000', u'#008080']

go_graph_1 = False
go_graph_2 = False
go_graph_3 = True
go_graph_4 = False

if go_graph_1:
    cm_arrays_list_1, percent_arrays_list_1 = get_1_arrays()
    cm_arrays_list_2, percent_arrays_list_2 = get_2_arrays()

    graph_1_cm_list = [cm_arrays_list_1[0],
                       cm_arrays_list_1[1],
                       cm_arrays_list_1[5],
                       cm_arrays_list_2[0],
                       cm_arrays_list_2[1]]

    graph_1_percent_list = [percent_arrays_list_1[0],
                            percent_arrays_list_1[1],
                            percent_arrays_list_1[5],
                            percent_arrays_list_2[0],
                            percent_arrays_list_2[1]]

    file_names = [r"d$_{max}$",
                  "4 cm",
                  r"d$_{max}$  -  Diode",
                  r"d$_{max}$  -  Bolus",
                  "4 cm  -  Bolus"]

    for i, percent_array in enumerate(graph_1_percent_list):
        plt.scatter(graph_1_cm_list[i], percent_array, s=0.7, label=file_names[i], color=color_list[i])

    plt.xlabel("Distance avec l'isocentre (cm)")
    plt.ylabel(r'Dose normalisée (D/D$_{d_{max}}$)')
    plt.xlim(-11, 11)
    plt.legend()
    plt.show()

if go_graph_2:
    cm_arrays_list_1, percent_arrays_list_1 = get_1_arrays()

    graph_2_cm_list = [cm_arrays_list_1[2],
                       cm_arrays_list_1[3],
                       cm_arrays_list_1[4],
                       cm_arrays_list_1[6],
                       cm_arrays_list_1[7]]

    graph_2_percent_list = [percent_arrays_list_1[2],
                            percent_arrays_list_1[3],
                            percent_arrays_list_1[4],
                            percent_arrays_list_1[6],
                            percent_arrays_list_1[7]]

    file_names = [r"d$_{max}$",
                  "7 cm",
                  r"d$_{max}$  -  4x4",
                  r"d$_{max}$  -  Diode",
                  r"d$_{max}$  -  4x4  Diode"]

    for i, percent_array in enumerate(graph_2_percent_list):
        plt.scatter(graph_2_cm_list[i], percent_array, s=0.7, label=file_names[i], color=color_list[i])

    plt.xlabel("Distance avec l'isocentre (cm)")
    plt.ylabel(r'Dose normalisée (D/D$_{d_{max}}$)')
    plt.xlim(-10, 10)
    plt.legend()
    plt.show()

if go_graph_3:
    cm_arrays_list_3, percent_arrays_list_3 = get_3_arrays()

    graph_3_cm_list = cm_arrays_list_3

    graph_3_percent_list = percent_arrays_list_3

    file_names = ["9 MeV",
                  "9 MeV  -  4x4",
                  "15 MeV",
                  "15 MeV  -  4x4",
                  "9 MeV  -  Diode",
                  "9 MeV  -  4x4  -  Diode",
                  "15 MeV  -  Diode",
                  "15 MeV  -  4x4  -  Diode"]

    for i, percent_array in enumerate(graph_3_percent_list):
        plt.scatter(graph_3_cm_list[i], percent_array, s=0.7, label=file_names[i], color=color_list[i])

    plt.xlabel("Profondeur (cm)")
    plt.ylabel(r'Dose normalisée (D/D$_{max}$)')
    plt.xlim(0, 11)
    plt.ylim(0, 113)
    plt.legend()
    plt.show()

    cm_arrays_list_4, percent_arrays_list_4 = get_4_arrays()

    graph_3_cm_list = [cm_arrays_list_3[0],
                       cm_arrays_list_3[2],
                       cm_arrays_list_4[0],
                       cm_arrays_list_4[1]]

    graph_3_percent_list = [percent_arrays_list_3[0],
                            percent_arrays_list_3[2],
                            percent_arrays_list_4[0],
                            percent_arrays_list_4[1]]

    file_names = ["9 MeV",
                  "15 MeV",
                  "9 MeV  -  DSP_105",
                  r"9 MeV  -  DSP_105  -  45$\degree$"]

    for i, percent_array in enumerate(graph_3_percent_list):
        plt.scatter(graph_3_cm_list[i], percent_array, s=0.7, label=file_names[i], color=color_list[i])

    plt.xlabel("Profondeur (cm)")
    plt.ylabel(r'Dose normalisée (D/D$_{max}$)')
    plt.xlim(0, 11)
    plt.ylim(0, 113)
    plt.legend()
    plt.show()

if go_graph_4:
    cm_arrays_list_5, percent_arrays_list_5 = get_5_arrays()

    graph_4_cm_list = cm_arrays_list_5

    graph_4_percent_list = percent_arrays_list_5

    file_names = ["Surface",
                  "d = 1.5 cm"]

    for i, percent_array in enumerate(graph_4_percent_list):
        plt.scatter(graph_4_cm_list[i], percent_array, s=0.7, label=file_names[i], color=color_list[i])

    plt.xlabel("Distance avec l'isocentre (cm)")
    plt.ylabel(r'Dose normalisée (D/D$_{d_{max}}$)')
    plt.xlim(-11, 11)
    # plt.ylim(-4, 113)
    plt.legend()
    plt.show()
