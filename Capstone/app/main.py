from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal 
from numpy.fft import fft
from kickingfrequency import *
import math
import format_data 
import MetaOutputParser 
import os 
import glob 
import warnings

# Setup 
path = os.getcwd() + '/data'
input_path = path + '/input/'
intermediate_path = path + '/intermediate/'
out_path = path + '/output/'
if os.path.exists(out_path) == False:
        os.makedirs(out_path)
if os.path.exists(intermediate_path + 'goggles') == False:
        os.makedirs(intermediate_path + 'goggles')
if os.path.exists(intermediate_path + 'fins') == False:
        os.makedirs(intermediate_path + 'fins')
# format_data(path)


def match_file(intermediate_path,out_path): 
        goggle_path = intermediate_path +'/goggles'
        fins_path = intermediate_path +'/fins'
        # Filename is last term in parsed expression
        # Add method here which reads in RT file by matching filename and then appends kick_freq by window to the RT CSV 
        rt_files = glob.glob(os.path.join(goggle_path, "*.csv"))
        fin_files = glob.glob(os.path.join(fins_path,"*.csv"))
        print(rt_files)
        for f in fin_files:
                parsedName = f.split("/")
                filename = parsedName[len(parsedName) - 1] 
                df = pd.read_csv(f)
                print(df)
                df = filter_data(df) 
                fin_parameters = filename.split("_")
                for i in rt_files:
                        rt_parameters = i.split("/")
                        rt_parameters = rt_parameters[len(rt_parameters) - 1].split("_")
                        print(rt_parameters)
                        if(fin_parameters[0] == rt_parameters[0]):
                                if(rt_parameters[1]== fin_parameters[1]): # if swimmer name matches 
                                        goggles_file = i
                                        fins_file = f 
                                        df_rt = pd.read_csv(goggles_file)
                                        df.columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z','pressure','depth','time']
                                        # THIS Line is where timestamp syncing should be called 
                                        df = pd.concat([df,df_rt], sort=False,axis =1)
                                        df.to_csv(out_path+rt_parameters[0]+rt_parameters[1]+'_complete.csv')

def filter_data(df): # data filtering 
        fs = 88; 
        b,a = signal.butter(4,3.14/fs,'lowpass')  
        df_filtered = pd.DataFrame()
        df_filtered['acc_x'] = signal.filtfilt(b, a, df['raw_acc_x'])
        df_filtered['acc_y'] = signal.filtfilt(b, a, df['raw_acc_y'])
        df_filtered['acc_z'] = signal.filtfilt(b, a, df['raw_acc_y'])
        df_filtered['gyr_x'] = df['raw_gyr_x']
        df_filtered['gyr_y'] = df['raw_gyr_y'] 
        df_filtered['gyr_z'] = df['raw_gyr_z']
        df_filtered['pressure'] = df['raw_pressure']
        df_filtered['depth'] = df['raw_pressure']/(pow(10,3)*9.81)
        df_filtered['time'] = df['time']
        return df_filtered

def kick_intervals(data): ## Returns a list of the start of kicking, a list of potential kick interval starts, a list of kick interval endpoints
        df = data
        peaks,_ = signal.find_peaks(df['pressure'],height=[103000,109000],width = [0.1,45])
        df['kicking'] = df.apply(lambda x: 0, axis=1)
        df['endpoints'] = df.apply(lambda x: 0, axis=1)
        start = peaks[0]
        for i in range(0,len(peaks)-3): 
                if peaks[i]>=peaks[i+1]-45:
                        if peaks[i+1]>=peaks[i+2]-45:
                                start = peaks[i]
                                df['kicking'].iloc[peaks[i]] = 1
                elif peaks[i]<=peaks[i+1]-100:
                        df['endpoints'].iloc[peaks[i]] = 1
                if i ==(len(peaks)-4):
                        df['endpoints'].iloc[peaks[i]] = 1
        s = df.index[df['kicking'] == 1].tolist()
        print(s)
        start = min(s)
        print(start)
        endpoints = df.index[df['endpoints'] == 1].tolist()
        print(endpoints)
        return start,s,endpoints
                       
def kick_count(df,s,endpoints): # Returns an array containing the kick count for each interval in which there was kick
        kick_count_by_interval = pd.Series()
        for i in range(0,len(endpoints)-1):
                if i == 0:
                        kick_count_by_interval[i] = len(zero_crossing(df,s[i],endpoints[i]))
                if(i>0 and i < len(endpoints)):
                        start = min(s.index[(s > endpoints[i-1] and s < endpoints[i])].tolist()) # interval is after preceeding endpoint and before next 
                        kick_count_by_interval[i] = len(zero_crossing(df,start,endpoints[i]))
                else: 
                        start = min(s.index[s > endpoints[i-1]].tolist()) # interval is after second to last endpoint till last endpoint 
                        kick_count_by_interval[i] = len(zero_crossing(df,start,endpoints[i]))
        return kick_count_by_interval

def zero_crossing(data,start,end):
        zero_crossings = np.where(np.diff(np.sign(data[5][start:end])))[0]
        return zero_crossings

MetaOutputParser.parseRT(input_path+'goggles',intermediate_path +'goggles/')
format_data.format_data(input_path + 'fins',intermediate_path+ 'fins/')
match_file(intermediate_path,out_path)
