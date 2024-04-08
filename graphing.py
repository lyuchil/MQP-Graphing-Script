import math
import sys
import os 
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans


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

def scaling(column):
    min = column.min()
    max = column.max()

    return ((column - min) / (max - min)) * 60



def dashboard(log_file_path, pm_file_path, graph_title):

    time_sync = sync(pm_file_path, log_file_path)

    time_end = time_sync + 60_000

    print(time_sync, time_end)

    # loading file according to file type
    if log_file_path.endswith(".csv"):
        data = pd.read_csv(log_file_path)
    elif log_file_path.endswith(".xlsx"):
        data = pd.read_excel(log_file_path)

    # load PresentMon Data
    pm_data = pd.read_csv(pm_file_path)

    # time sync

    # data_sleep_off_set = data[['time (ms)','sleep_offset']].dropna()
    # data_sleep = data[['time (ms)','actualSleepTime']].dropna()
    # data_asleep = data[['time (ms)','average_slp']].dropna()
    synced_data = data.loc[(data['time (ms)'] >= time_sync) & (data['time (ms)'] <= time_end)]    
    

    # removing NAN values
    queueSize = synced_data[['time (ms)', 'queueSize']].dropna()
    sleep_offset = synced_data[['time (ms)','sleep_offset']].dropna()
    interframeTimeEn = synced_data[['time (ms)','interFrameTimeEnqueue']].dropna()
    interframeTimeDe = synced_data[['time (ms)','interFrameTimeDequeue']].dropna()
    intended_sleep = synced_data[['time (ms)','average_slp']].dropna()
    actual_sleep = synced_data[['time (ms)','actualSleepTime']].dropna()
    pm_interframe_time = pm_data[['TimeInSeconds','msBetweenPresents']]
 

    average_queue_size = queueSize['queueSize'].mean()
    
    double_standard_frame_time = 1 / 30 * 1_000
    
    pm = pm_data['msBetweenPresents']
    interrupt_boolean = pm > double_standard_frame_time
    interrupt_frame_time = pm[interrupt_boolean]
    interrupt_count = interrupt_boolean.sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])
    magnitude = (interrupt_frame_time - double_standard_frame_time).sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])



    # remove inital interframe time 
    interframeTimeEn = interframeTimeEn.iloc[1:, :]
    interframeTimeDe = interframeTimeDe.iloc[1:, :]

    figures, axis = plt.subplots(3,2)
    trans = mtrans.blended_transform_factory(figures.transFigure,
                                         mtrans.IdentityTransform())
    figures.tight_layout(rect=[0, 0.03, 1, 0.95])
    figures.suptitle(graph_title)
    txt = figures.text(.5, 40, f"Average Queue Size: {average_queue_size}", ha='center')
    txt2 = figures.text(.5, 25, f"Interrupts: {interrupt_count} /s", ha='center')
    txt3 = figures.text(.5, 10, f"Magnitude: {magnitude} ms/s", ha='center')
    txt.set_transform(trans)
    txt2.set_transform(trans)
    txt3.set_transform(trans)

    # plotting queue size graph
    axis[0,0].plot("time (ms)", "queueSize", data=queueSize)
    axis[0,0].set_title('Queue Size')

    # plotting PresentMon interframe time 
    axis[0,1].plot('TimeInSeconds', 'msBetweenPresents', data=pm_interframe_time)
    axis[0,1].set_title('PresentMon Interframe Time')

    # plotting interframe time enqueue 
    axis[1,0].plot("time (ms)", "interFrameTimeEnqueue", data=interframeTimeEn)
    axis[1,0].set_title('Interframe Time Enqueue')

    # plotting interframe time dequeue
    axis[1,1].plot("time (ms)", "interFrameTimeDequeue", data=interframeTimeDe)
    axis[1,1].set_title('Interframe Time Dequeue')

    # plotting sleep value
    axis[2,0].plot("time (ms)", "sleep_offset", data=sleep_offset)
    axis[2,0].set_title('sleep_offset')

    # plotting intended sleep vs actual sleep
    axis[2,1].plot("time (ms)", "average_slp", color="red", data=intended_sleep)
    axis[2,1].plot("time (ms)", "actualSleepTime",color="blue" ,data=actual_sleep)
    axis[2,1].set_title('Intended vs Actual Sleep')

    plt.show()



def graphing(log_file_path, pm_file_path, graph_title):
    time_sync = sync(pm_file_path, log_file_path)

    time_end = time_sync + 60_000

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
    interframeTimeEn = synced_data[['time (ms)','interFrameTimeEnqueue']].dropna()
    interframeTimeDe = synced_data[['time (ms)','interFrameTimeDequeue']].dropna()
 

    average_queue_size = queueSize['queueSize'].mean()
    double_standard_frame_time = 1 / 30 * 1_000
    
    pm = pm_data['msBetweenPresents']
    interrupt_boolean = pm > double_standard_frame_time
    interrupt_frame_time = pm[interrupt_boolean]
    interrupt_count = interrupt_boolean.sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])
    magnitude = (interrupt_frame_time - double_standard_frame_time).sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])


    # remove inital interframe time 
    interframeTimeEn = interframeTimeEn.iloc[1:, :]
    interframeTimeDe = interframeTimeDe.iloc[1:, :]

    # recalibration and scaling
    queueSize['time (ms)'] = scaling(queueSize['time (ms)'])

    interframeTimeEn['time (ms)'] = scaling(interframeTimeEn['time (ms)'])
    interframeTimeEn['interFrameTimeEnqueue'] = interframeTimeEn['interFrameTimeEnqueue'] / 1000

    interframeTimeDe['time (ms)'] = scaling(interframeTimeDe['time (ms)'])
    interframeTimeDe['interFrameTimeDequeue'] = interframeTimeDe['interFrameTimeDequeue'] / 1000

    figures, axis = plt.subplots(3,1, figsize=(10,5), sharex=True)
    trans = mtrans.blended_transform_factory(figures.transFigure,
                                         mtrans.IdentityTransform())
    figures.tight_layout(rect=[0, 0.02, 1, 0.99])
    figures.suptitle(graph_title, fontsize=18, fontweight='bold')
    txt = figures.text(0.15, 15, f"Average Queue Size: {average_queue_size}", ha='center', fontsize=18)
    txt2 = figures.text(.5, 15, f"Interrupts: {interrupt_count} /s", ha='center', fontsize=18)
    txt3 = figures.text(.8, 15, f"Magnitude: {magnitude} ms/s", ha='center', fontsize=18)
    txt.set_transform(trans)
    txt2.set_transform(trans)
    txt3.set_transform(trans)

   
    # plotting interframe time enqueue 
    axis[0].plot("time (ms)", "interFrameTimeEnqueue", data=interframeTimeEn, color='Maroon')
    #axis[0].set_title('Enqueue', loc='right')
    axis[0].set_xlim(0, 60)
    axis[0].set_ylim(0, 100)
    #axis[1].set_xlabel('Time (s)')
    axis[0].set_ylabel('Frame Time (ms)', fontsize=18)


    # plotting queue size graph
    axis[1].plot("time (ms)", "queueSize", data=queueSize, color='Green')
    #axis[1].set_title('Queue Size')
    axis[1].set_xlim(0, 60)
    axis[1].set_ylim(0, 18)
    #axis[0].set_xlabel('Time (s)')
    axis[1].set_ylabel('Frames', fontsize=18)


    # plotting interframe time dequeue
    axis[2].plot("time (ms)", "interFrameTimeDequeue", data=interframeTimeDe, color='Navy')
    #axis[2].set_title('Dequeue')
    axis[2].set_xlim(0, 60)
    axis[2].set_ylim(0, 100)
    axis[2].set_xlabel('Time (s)', fontsize=18)
    axis[2].set_ylabel('Frame Time (ms)', fontsize=18)

    figures.text(0.98, 0.8, 'Enqueue', ha='center', va='center', rotation=-90, fontsize=18)
    figures.text(0.98, 0.5, 'Queue Size', ha='center', va='center', rotation=-90, fontsize=18)
    figures.text(0.98, 0.2, 'Dequeue', ha='center', va='center', rotation=-90, fontsize=18)


    for ax in axis:
        ax.tick_params(axis='x', labelsize=18)
        ax.tick_params(axis='y', labelsize=18)


    plt.subplots_adjust(hspace=0.1)


    plt.show()



def base_graphing(log_file_path, pm_file_path, graph_title):
  
    # loading file according to file type
    if log_file_path.endswith(".csv"):
        data = pd.read_csv(log_file_path)
    elif log_file_path.endswith(".xlsx"):
        data = pd.read_excel(log_file_path)

    # load PresentMon Data
    pm_data = pd.read_csv(pm_file_path)

    double_standard_frame_time = 1 / 30 * 1_000
    
    pm = pm_data['msBetweenPresents']
    interrupt_boolean = pm > double_standard_frame_time
    interrupt_frame_time = pm[interrupt_boolean]
    interrupt_count = interrupt_boolean.sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])
    magnitude = (interrupt_frame_time - double_standard_frame_time).sum() / (pm_data['TimeInSeconds'].iloc[-1] - pm_data['TimeInSeconds'].iloc[0])

    plt.title('Moonlight 100 ms Jitter', fontweight='bold', fontsize=18)

    plt.plot(pm_data['TimeInSeconds'], pm_data['msBetweenPresents'])

    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Frame Time (ms)', fontsize=18)

    xlabel_pos = plt.gca().xaxis.get_label().get_position()

    # for nj
    # plt.text(xlabel_pos[0] + 5, xlabel_pos[1] - 10, f"Interrupts: {interrupt_count} /s", fontsize=18)
    # plt.text(xlabel_pos[0] + 50, xlabel_pos[1] - 10, f"Magnitude: {magnitude} ms/s", ha='center', fontsize=18)
    

    # for jitter
    plt.text(xlabel_pos[0] + 5, xlabel_pos[1] - 20, f"Interrupts: {interrupt_count} /s", fontsize=18)
    plt.text(xlabel_pos[0] + 50, xlabel_pos[1] - 20, f"Magnitude: {magnitude} ms/s", ha='center', fontsize=18)

    plt.tick_params(axis='x', labelsize=18)  # Adjust labelsize as needed
    plt.tick_params(axis='y', labelsize=18)

    plt.show()



if __name__ == "__main__":
    args = parser.parse_args()

    # check if paths provided are valid 
    if not os.path.exists(args.log):
        parser.error("Log file does not exist. Please check the input path")
  
    
    if not os.path.exists(args.pm):
        parser.error("PresentMon file does not exist. Please check the input path")
    

    #dashboard(args.log, args.pm, args.title)
    graphing(args.log, args.pm, args.title)
    #base_graphing(args.log, args.pm, args.title)
    #sync(args.pm, args.log)

    