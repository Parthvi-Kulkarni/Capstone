import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import datetime
import kickingfrequency

# Import csv
df2 = pd.read_csv('Capstone/app/data/testD.csv')
df3 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/testE.csv')
df = pd.read_csv('Capstone/app/data/testF.csv')

raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_acc_z = df[df.columns[2]]
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]
raw_bar = df[df.columns[6]]
raw_A1 = [raw_acc_x, raw_acc_y, raw_acc_z]
raw_G1 = [raw_gyr_x, raw_gyr_y, raw_gyr_z]
time = df[df.columns[7]]
length = len(time)

# Plot of raw data
fig, ax = plt.subplots()
ax.set_title('Raw Gyroscope Data in the Z direction')
ax.set_xlabel('Time')
ax.set_ylabel('Angular Velocity in the Z direction')
ax.plot(time, raw_gyr_z, 'b')
#plt.show() 

# Applying an IIR Filter
b, a = signal.butter(3, 0.05) 
zi = signal.lfilter_zi(b, a) # chooses the initial condition of the IIR filter
z, _ = signal.lfilter(b, a, raw_gyr_z, zi=zi*raw_acc_z[0])
z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
signal_gyr_z = signal.filtfilt(b, a, raw_gyr_z) # apply the filter

# Plot of IIR Filtered Data
plt.plot(time, signal_gyr_z, 'b')
# plt.show()

# Peak detection during active periods
numpeaks = signal.find_peaks(signal_gyr_z) # Gives the indices of the peaks
firstpeak = numpeaks[0][0]
lastpeak = numpeaks[0][-1]

# Zero-crossing
zero_crossings = np.where(np.diff(np.signbit(signal_gyr_z)))

milliseconds = []


for i in range(0,length):
    timestamp = datetime.datetime.strptime(time[i], '%H:%M:%S.%f')
    ms = timestamp.timestamp() * 1000
    milliseconds.append(ms)

# Add a column to the dataframe
df['Milliseconds'] = milliseconds

ms = df[df.columns[8]]
average_frequency = kickingfrequency.peak_detection(ms, numpeaks)
print('Kicking frequency: ' + str(average_frequency) + ' kicks per second')
average_frequency = kickingfrequency.zero_crossing(ms, zero_crossings)
print('Kicking frequency: ' + str(average_frequency) + ' kicks per second')
