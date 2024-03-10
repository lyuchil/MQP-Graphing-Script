import math
import sys
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

mean_result_list = []
standard_error_list = []
standard_deviation_list = []
std_sem = []
base_moonlight_mean = 0
base_moonlight_standard_error = 0
base_moonlight_std = 0
base_moonlight_sem = 0

def make_graph():
    figure, (ax1, ax2) = plt.subplots(1, 2)
    interp_func = interp1d(np.arange(len(mean_result_list)), mean_result_list, kind='cubic')
    x_fine = np.linspace(0, len(mean_result_list) - 1, 100)
    y_fine = interp_func(x_fine)

    mean, standard_error, std, std_sem = process_folder("C:\\Log Output\\base_moonlight")
    base_moonlight_mean = mean

    interp_func_2 = interp1d(np.arange(len(standard_deviation_list)), standard_deviation_list, kind='cubic')
    x_fine_2 = np.linspace(0, len(standard_deviation_list) - 1, 100)
    y_fine_2 = interp_func_2(x_fine_2)

    labels = ["1.2", "1.22", "1.24", "1.26", "1.28","1.3"]
    
    ax1.scatter(labels, mean_result_list, s=200)
    ax1.errorbar(labels, mean_result_list, yerr=standard_error_list, xerr=None,  capsize=5, ls='none')
    ax1.axhline(y=base_moonlight_mean, linestyle='--', c='purple', label='Mean')
    ax1.set_xlabel('Fudge Factor (ms)', fontsize=14)
    ax1.set_ylabel('Late Frames/min', fontsize=14)
    ax1.set_title("Late Frames/min vs Fudge Factor", fontsize=14)

    ax2.scatter(labels, standard_deviation_list, s=200)
    ax2.errorbar(labels, standard_deviation_list, yerr=std_sem, xerr=None,  capsize=5, ls='none')
    ax2.axhline(y=std, linestyle='--', c='purple', label='Mean')
    ax2.set_xlabel('Fudge Factor (ms)', fontsize=14)
    ax2.set_ylabel('Standard Deviation', fontsize=14)
    ax2.set_title("Standard Deviation vs Fudge Factor", fontsize=14)

    plt.show()



def process_csv(file_path):
    data = pd.read_csv(file_path)

    data_mean = data['msBetweenDisplayChange'].mean()
    data_std = data['msBetweenDisplayChange'].std()
    late_count = 0
    for time in data['msBetweenDisplayChange']:
        if time > data_mean + data_std:
            late_count += 1


    return late_count, data_std 


def process_folder(folder_path):
    temp_result = []
    temp_result_2 = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            count, std = process_csv(file_path)
            temp_result.append(count)
            temp_result_2.append(std)

    result = pd.DataFrame(temp_result)
    result2 = pd.DataFrame(temp_result_2)
    mean = result.mean().iloc[0]
    std_mean = result2.mean().iloc[0]
    standard_error = result.sem().iloc[0]
    std_sem = result2.sem().iloc[0]
    return mean, standard_error, std_mean, std_sem


def process_directory(root_path):
    for folder in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder)
        if os.path.isdir(folder_path):
            print(folder_path)
            folder_mean, folder_sem, folder_std, folder_std_sem = process_folder(folder_path)
            mean_result_list.append(folder_mean)
            standard_error_list.append(folder_sem)
            standard_deviation_list.append(folder_std)
            std_sem.append(folder_std_sem)


# def base_moonlight_calculation(folder_path):
    




if __name__ == "__main__":
    # main location of data 
    root_directory = "C:\Log Output\Feb - 6"
    base_moonlight = "C:\\Log Output\\base_moonlight"
    process_directory(root_directory)
    # base_moonlight_calculation(base_moonlight)

    make_graph()
