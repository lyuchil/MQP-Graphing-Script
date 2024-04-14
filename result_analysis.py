import pandas as pd
import numpy as np
import os, sys
import matplotlib.pyplot as plt
from scipy import stats

column = sys.argv[1]
y_label = sys.argv[2]
title = sys.argv[3]



# Step 1: Define the directory containing the policy folders
directory = "C:/Users/claypool/Desktop/my_test/Results"

# Step 2: Get a list of all subdirectories (policy folders) in the directory
policy_folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]

# if "Average Queue Size" in sys.argv:
#     # Remove "base moonlight" folder from the list
#     policy_folders.remove("Base Moonlight")

# Step 3: Define a color palette for policies
color_palette = plt.cm.tab10.colors  # You can use any colormap, or define your own list of colors

# Step 4: Create a dictionary to map each policy folder to a color
policy_colors = dict(zip(policy_folders, color_palette))

# Step 5: Initialize a dictionary to store data points for each policy folder
all_data_points = {}
legend_handles = {}

# Step 6: Iterate over each policy folder
for policy_folder in policy_folders:
    # Step 7: Get a list of CSV files in the current policy folder
    csv_files = [file for file in os.listdir(os.path.join(directory, policy_folder)) if file.endswith('.csv')]
    
    # Step 8: Initialize a list to store the data points
    data_points = []

    # Step 9: Iterate through each CSV file, read the data, and extract the mean for each setting
    # for file in csv_files:
    #     setting = file.split('.')[0]  # Extract setting from file name
    #     data = pd.read_csv(os.path.join(directory, policy_folder, file))
        
    #     # Store mean for the setting
    #     mean = data[column].mean()
       
    #     # Store mean and margin of error for the setting
    #     data_points.append((setting, mean))
    for file in csv_files:

        setting = file.split('.')[0]

        if "Average Queue Size" in sys.argv and policy_folder == "Base Moonlight":
           mean = 0
           confidence = 0
           data_points.append((setting, mean, confidence))
        else:
            #setting = file.split('.')[0]  # Extract setting from file name
            data = pd.read_csv(os.path.join(directory, policy_folder, file))
        
            # Calculate mean and confidence interval
            mean = data[column].mean()
            confidence = 1.96 * data[column].sem()  # 95% confidence interval
        
            # Store mean and confidence interval for the setting
            data_points.append((setting, mean, confidence))


        

    # Step 10: Sort the data points based on the settings
    data_points.sort(key=lambda x: ('No', 'Low', 'Medium', 'High').index(x[0]))

    # Step 11: Store data points for the current policy folder in the dictionary
    all_data_points[policy_folder] = data_points

    if policy_folder not in legend_handles:
        x_values = [setting for setting, mean, confidence in data_points]
        y_values = [mean for setting, mean, confidence in data_points]
        color = policy_colors[policy_folder]  # Define color for this policy folder
        handle = plt.plot(x_values, y_values, color=color, label=policy_folder)
        legend_handles[policy_folder] = handle



# Step 12: Plot all data points for each policy folder on the same graph
plt.figure(figsize=(24, 10))
# for policy_folder, data_points in all_data_points.items():
#     # Plot all points with the same color and label each point with the policy name
#     color = policy_colors[policy_folder]
#     for setting, mean in data_points:
#         plt.scatter(setting, mean, color=color)
   


#     # Draw lines between consecutive data points
#     x_values = [setting for setting, mean in data_points]
#     y_values = [mean for setting, mean in data_points]
#     plt.plot(x_values, y_values, color=color)

for policy_folder, data_points in all_data_points.items():
    # Plot all points with the same color and label each point with the policy name
    color = policy_colors[policy_folder]
    
    # Plot data points and error bars
    for setting, mean, confidence in data_points:
        plt.errorbar(setting, mean, yerr=confidence, fmt='o', color=color, label=policy_folder, ecolor=color, linewidth=2.5,capsize=10)
    
    # Extract x values (settings), y values (means), and error values (confidence intervals) from data_points
    x_values = [setting for setting, _, _ in data_points]
    y_values = [mean for _, mean, _ in data_points]
    errors = [confidence for _, _, confidence in data_points]

    # Plot data points with transparency
    plt.scatter(x_values, y_values, color=color, alpha=0.1, s=200)

    #Plot connected line
    x_values = [setting for setting, _, _ in data_points]
    y_values = [mean for _, mean, _ in data_points]
    plt.plot(x_values, y_values, color=color)

plt.legend(handles=[legend_handles[policy_folder][0] for policy_folder in policy_folders], title='Policy', bbox_to_anchor=(1.02, 0.5), loc='upper left', fontsize=12)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Jitter Settings', fontsize=14)
plt.ylabel(f'{y_label}', fontsize=14)
plt.title(f'{title}', fontsize=14)
#plt.legend(title='Policy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.subplots_adjust(right=0.75)
plt.show()