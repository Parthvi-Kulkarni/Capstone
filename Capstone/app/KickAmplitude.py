import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from numpy.fft import fft
import datetime
import time

# Import csv
df = pd.read_csv('C:/Users/jade-/PycharmProjects/Capstone/Capstone/app/data/testD.csv')

# Create Filter Parameters
b,a = signal.butter(4,0.1,'lowpass')

# Retrieve raw data files
raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_acc_z = df[df.columns[2]]
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]

time = df[df.columns[7]]

raw_A = [raw_acc_x, raw_acc_y, raw_acc_z]
raw_G = [raw_gyr_x, raw_gyr_y, raw_gyr_z]

length = len(time)

# Filter Signals
acc_x = signal.filtfilt(b, a, raw_acc_x)
acc_y = signal.filtfilt(b, a, raw_acc_y)
acc_z = signal.filtfilt(b, a, raw_acc_z)
gyr_x = signal.filtfilt(b, a, raw_gyr_x)
gyr_y = signal.filtfilt(b, a, raw_gyr_y)
gyr_z = signal.filtfilt(b, a, raw_gyr_z)

# Get time in seconds
seconds = []
start = datetime.datetime.strptime(time[0],'%H:%M:%S.%f')

for i in range(0,length):
    ts = datetime.datetime.strptime(time[i], '%H:%M:%S.%f')
    duration = ts - start
    sec = duration.total_seconds()
    seconds.append(sec)

