import time
import subprocess
import pydirectinput
import ctypes, sys,os
import time 
import json
import re

def rewrite_config(new_config):
    with open("C:/Users/claypool/Desktop/my_test/config.txt", 'w') as f:
        f.write(new_config)


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


config_json = 'config.json'
config = load_json(config_json)

jitter_settings = ["no", "low", "medium", "high"]

policies = ["base", "E", "E-Q10", "E-Q2"]

if __name__ == '__main__':

  
    # open admin command prompt before running the script 
    # otherwise everything crashes
    for setting in jitter_settings:
        for policy in policies:
       
            print(f"Crrently Running {setting} jitter with {policy} policy")

            if setting == "no":
                sJ = subprocess.Popen('python C:/Users/claypool/Desktop/auto_play/jitter_stop.py')
                sJ.wait()
            elif setting == "low":
                sJ = subprocess.Popen('python C:/Users/claypool/Desktop/auto_play/jm25.py')
                sJ.wait()
            elif setting == "medium":
                sJ = subprocess.Popen('python C:/Users/claypool/Desktop/auto_play/jm50.py')
                sJ.wait()
            elif setting == "high":
                sJ = subprocess.Popen('python C:/Users/claypool/Desktop/auto_play/jm100.py')
                sJ.wait()

            print(f"Finished applying jitter at {setting}")


            if policy == "E":
                rewrite_config("EPolicy,false,2,2500,1200,4000,")
                print(f"Rewrittent config.txt with EPolicy,false,2,2500,1200,4000, for {policy} policy")
            elif policy == "E-Q10":
                rewrite_config("EPolicy,true,10,2500,1200,4000,")
                print(f"Rewrittent config.txt with EPolicy,true,10,2500,1200,4000, for {policy} policy")
            elif policy == "E-Q2":
                rewrite_config("EPolicy,true,2,2500,1200,4000,")
                print(f"Rewrittent config.txt with EPolicy,true,2,2500,1200,4000, for {policy} policy")


            print(f"Starting benchmark for {policy} policy")

            logger_result_folder = f"{policy}-{setting}"
            pm_logger_result_folder = f"pm-{policy}-{setting}" 

            os.mkdir(logger_result_folder)
            os.mkdir(pm_logger_result_folder)

            for _ in range(50):

                # launches moonlight
                if policy == "base":
                    s1 = subprocess.Popen('python open_base_moonlight.py')
                    s1.wait()
                    print("Opened base moonlight")
                else:
                    s1 = subprocess.Popen('python open_moonlight.py')
                    s1.wait()
                    print("Opened Moonlight")


                
                # make sure moonlight stream is open
                time.sleep(5)

                # opens benchmark in wt
                s2 = subprocess.Popen('python war_thunder_keybinds.py')
                s2.wait()

                # make sure moonlight is closed so that we can access the fie 
                os.system("taskkill /f /im  Moonlight.exe")
                time.sleep(5)

                # rename and match files
                s3 = subprocess.Popen(f'python match_file.py {logger_result_folder} {pm_logger_result_folder}')  
                s3.wait()
                time.sleep(5)

                #s4 = subprocess.Popen('python auto_graph.py')  
                #s4.wait()
            if policy == "base":
                s4 = subprocess.Popen(f'python base_analysis.py {logger_result_folder} {pm_logger_result_folder}')
                s4.wait()
            else:
                s4 = subprocess.Popen(f'python analysis.py {logger_result_folder} {pm_logger_result_folder}')
                s4.wait()
            
            time.sleep(5)

            print(f"{setting} Done")
            print("Reset Jitter Setting")
            sE = subprocess.Popen('python C:/Users/claypool/Desktop/auto_play/jitter_stop.py')
            sE.wait()
            print("Done reset jitter setting")

    



