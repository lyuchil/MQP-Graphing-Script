import os
import json

config_json = 'config.json'

# some globals for basic settings 
# can rearrange these into the config file and change before each run (currnetly listed for testing pruposes)
logger_source_folder = "C:/MQP/logger_output_loc_1"
pm_source_folder = "C:/MQP/pm_folder_1"

logger_final_folder = "C:/MQP/logger_output_loc_2"
pm_final_folder = "C:/MQP/pm_folder_2"


def load_json(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config
    
def save_config(file_path, config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=2)


def update_json(file_path, key, new_value):
    config = load_json(file_path)
    config[key] = new_value
    save_config(file_path, config)

# add expected tag to the given file 
def add_tag(file_path, tag, destination_folder):
    base_path, file_name = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(file_name)

    new_file_name = f"{file_name}_{tag}{file_extension}"
    new_file_path = os.path.join(destination_folder, new_file_name)

    return new_file_path

# rename and move the file to final location
def rename_logger_file(folder_path, tag, destination_folder):
    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        new_file_path = add_tag(file_path, tag, destination_folder)

        os.rename(file_path, new_file_path)

# load config and extract label
config = load_json(config_json)

current_label_value = config['label']

# rename logger file
rename_logger_file(logger_source_folder, current_label_value, logger_final_folder)

# rename PresentMon file
rename_logger_file(pm_source_folder, current_label_value, pm_final_folder)

# update value in config.json
new_value = config['label'] + 1
update_json(config_json, "label", new_value)
save_config(config_json, config)

