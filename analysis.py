import math
import sys
import os 

files = os.listdir('C:/Users/claypool/Desktop/local_logger_mqp23-24')
pm_files = os.listdir('C:/Users/claypool/Desktop/pm_logger_mqp_23-24')


def get_file_and_tag(file_name):
    file_creation_time, tag = file_name.split("%")
    return file_creation_time, tag


def match_pm_file(tag):
    for pm_file in pm_files:
        pm_file_name, file_extension = os.path.splitext(pm_file)
        pm_file_time, pm_tag = get_file_and_tag(pm_file_name)
        if tag == pm_tag:
            return pm_file_time


for file in files:
    file_name, extension = os.path.splitext(file)
    file_time, tag = get_file_and_tag(file_name)
    matched_file = match_pm_file(tag)
    print(int(matched_file) - int(file_time))











