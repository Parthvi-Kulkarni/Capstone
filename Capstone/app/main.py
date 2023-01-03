import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

# Import csv
#df1 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test1.csv')
df = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test2.csv')
#df3 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test3.csv')
#df4 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test4.csv')
#df5 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test5.csv')

raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_acc_z = df[df.columns[2]]
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]
raw_A1 = [raw_acc_x, raw_acc_y, raw_acc_z]
raw_G1 = [raw_gyr_x, raw_gyr_y, raw_gyr_z]
time = df[df.columns[6]]

# Plot of raw data
plt.figure
plt.plot(time, raw_gyr_z, 'b')
plt.grid(True)
plt.show()

# Denoise the data by applying an IIR Filter
b, a = signal.butter(3, 0.05)
zi = signal.lfilter_zi(b, a) # chooses the initial condition of the IIR filter
z, _ = signal.lfilter(b, a, raw_gyr_z, zi=zi*raw_acc_z[0])
z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
signal_gyr_z = signal.filtfilt(b, a, raw_gyr_z) # apply the filter

# Plot of IIR Filtered Data
plt.figure
plt.plot(time, signal_gyr_z, 'b')
plt.grid(True)
plt.show()