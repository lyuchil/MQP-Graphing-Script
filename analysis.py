import math
import sys
import os 
import pandas as pd 

# paths and folders

logger_folder = sys.argv[1]
pm_folder = sys.argv[2]

logger_files = os.listdir(logger_folder)
pm_files = os.listdir(pm_folder)


# results array
results = []

# gets the tag for each csv file
def get_file_and_tag(file_name):
    file_creation_time, tag = file_name.split("%")
    return tag


# def match_pm_file(tag):
#     for pm_file in pm_files:
#         pm_file_name, file_extension = os.path.splitext(pm_file)
#         pm_file_time, pm_tag = get_file_and_tag(pm_file_name)
#         if tag == pm_tag:
#             return pm_file_time


for logger_file in logger_files:

    # get the tag and match that tag with files in the pm folder
    tag = get_file_and_tag(logger_file)
    matching_file = next((pm_file for pm_file in pm_files if get_file_and_tag(pm_file) == tag), None)
    

    # if a match is found, then wewill sync the time for both files and calculate the average queue size, interrupts /s and magnitude of the interrupts
    if matching_file:
        log_file = os.path.join(logger_folder, logger_file)
        pm_file = os.path.join(pm_folder, matching_file)

        log_time = logger_file.split("%")[0]
        pm_time = matching_file.split("%")[0]

        capture_starting_time = int(pm_time) - int(log_time)
        capture_ending_time = capture_starting_time + 60_000
        
        our_logger_df = pd.read_csv(log_file)
        pm_logger_df = pd.read_csv(pm_file)

        
        our_logger_df = our_logger_df.loc[(our_logger_df['time (ms)'] >= capture_starting_time) & (our_logger_df['time (ms)'] <= capture_ending_time)]   

        queuesize = our_logger_df[['time (ms)', 'queueSize']].dropna()       
        pm_frame_time = pm_logger_df[['TimeInSeconds','msBetweenPresents']]

        average_queue_size = queuesize['queueSize'].mean()
    
        double_standard_frame_time = 1 / 30 * 1_000
        pm_frame_time = pm_logger_df['msBetweenPresents']
        interrupt_boolean = pm_frame_time > double_standard_frame_time
        interrupt_frame_time = pm_frame_time[interrupt_boolean]
        interrupt_count = interrupt_boolean.sum() / (pm_logger_df['TimeInSeconds'].iloc[-1] - pm_logger_df['TimeInSeconds'].iloc[0])
        magnitude = (interrupt_frame_time - double_standard_frame_time).sum() / (pm_logger_df['TimeInSeconds'].iloc[-1] - pm_logger_df['TimeInSeconds'].iloc[0])

        # add the calculated result
        results.append({
            "Tag" : tag,
            "Average Queue Size" : average_queue_size,
            "Interrupts" : interrupt_count,
            "Magnitude" : magnitude
        })


# convert to dataframe and store to a csv
result_df = pd.DataFrame(results)
output_file_path = os.path.join(pm_folder, "results.csv")
result_df.to_csv(output_file_path, index=False)













