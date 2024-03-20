import math
import sys
import os 
import argparse
import pandas as pd
import matplotlib.pyplot as plt



# initalizing the parser 
parser = argparse.ArgumentParser(
    prog='Dashboard Generator',
    description='This script creates the dash board after each run and turn the csv files into graphs',
)

# adding command line arguments
parser.add_argument('--log')
parser.add_argument('--pm')
parser.add_argument('--title')


def get_file_and_tag(file_name):
    file_creation_time, tag = file_name.split("%")
    return file_creation_time, tag


def sync(pm, log):
    
    log_name, extension1 = get_file_and_tag(log)
    pm_name, extension2 = get_file_and_tag(pm)


    log_time = log_name.split("\\").pop()
    pm_time = pm_name.split("\\").pop()

 
    return int(pm_time) - int(log_time)


def graphing(log_file_path, pm_file_path, graph_title):

    time_sync = sync(pm_file_path, log_file_path)

    time_end = time_sync + 30_000

    print(time_sync, time_end)

    # loading file according to file type
    if log_file_path.endswith(".csv"):
        data = pd.read_csv(log_file_path)
    elif log_file_path.endswith(".xlsx"):
        data = pd.read_excel(log_file_path)

    # load PresentMon Data
    pm_data = pd.read_csv(pm_file_path)

    # time sync

    synced_data = data.loc[(data['time (ms)'] >= time_sync) & (data['time (ms)'] <= time_end)]    
    

    # removing NAN values
    queueSize = synced_data[['time (ms)', 'queueSize']].dropna()
    sleepValue = synced_data[['time (ms)','sleepValue']].dropna()
    interframeTimeEn = synced_data[['time (ms)','interFrameTimeEnqueue']].dropna()
    interframeTimeDe = synced_data[['time (ms)','interFrameTimeDequeue']].dropna()
    intended_sleep = synced_data[['time (ms)','average_slp']].dropna()
    actual_sleep = synced_data[['time (ms)','actualSleepTime']].dropna()
    pm_interframe_time = pm_data[['TimeInSeconds','msBetweenDisplayChange']]


    # remove inital interframe time 
    interframeTimeEn = interframeTimeEn.iloc[1:, :]
    interframeTimeDe = interframeTimeDe.iloc[1:, :]

    figures, axis = plt.subplots(3,2)
    figures.tight_layout(rect=[0, 0.03, 1, 0.95])
    figures.suptitle(graph_title)

    # plotting queue size graph
    axis[0,0].plot("time (ms)", "queueSize", data=queueSize)
    axis[0,0].set_title('Queue Size')

    # plotting PresentMon interframe time 
    axis[0,1].plot('TimeInSeconds', 'msBetweenDisplayChange', data=pm_interframe_time)
    axis[0,1].set_title('PresentMon Interframe Time')

    # plotting interframe time enqueue 
    axis[1,0].plot("time (ms)", "interFrameTimeEnqueue", data=interframeTimeEn)
    axis[1,0].set_title('Interframe Time Enqueue')

    # plotting interframe time dequeue
    axis[1,1].plot("time (ms)", "interFrameTimeDequeue", data=interframeTimeDe)
    axis[1,1].set_title('Interframe Time Dequeue')

    # plotting sleep value
    axis[2,0].plot("time (ms)", "sleepValue", data=sleepValue)
    axis[2,0].set_title('Sleep value')

    # plotting intended sleep vs actual sleep
    axis[2,1].plot("time (ms)", "average_slp", color="red", data=intended_sleep)
    axis[2,1].plot("time (ms)", "actualSleepTime",color="blue" ,data=actual_sleep)
    axis[2,1].set_title('Intended vs Actual Sleep')

    plt.show()





if __name__ == "__main__":
    args = parser.parse_args()

    # check if paths provided are valid 
    if not os.path.exists(args.log):
        parser.error("Log file does not exist. Please check the input path")
  
    
    if not os.path.exists(args.pm):
        parser.error("PresentMon file does not exist. Please check the input path")
    

    graphing(args.log, args.pm, args.title)
    #sync(args.pm, args.log)

    