import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

# Import csv
df = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test2.csv')

raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_acc_z = df[df.columns[2]]
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]
raw_A1 = [raw_acc_x, raw_acc_y, raw_acc_z]
raw_G1 = [raw_gyr_x, raw_gyr_y, raw_gyr_z]
time = df[df.columns[6]]

# TODO: convert time from %H:%M:%S:%f to seconds.milliseconds

# Plot of raw data
fig, ax = plt.subplots()
ax.set_title('Raw Gyroscope Data in the Z direction')
ax.set_xlabel('Time')
ax.set_ylabel('Angular Velocity in the Z direction')
ax.plot(time, raw_gyr_z, 'b')
plt.show() 

# Denoise the data by applying an IIR Filter
b, a = signal.butter(3, 0.05)
zi = signal.lfilter_zi(b, a) # chooses the initial condition of the IIR filter
z, _ = signal.lfilter(b, a, raw_gyr_z, zi=zi*raw_acc_z[0])
z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
signal_gyr_z = signal.filtfilt(b, a, raw_gyr_z) # apply the filter

# Plot of IIR Filtered Data
plt.plot(time, signal_gyr_z, 'b')
plt.show()

# TODO: Apply Butterworth Filter to Data

# Slope detection :  Look for places where the second derivative (der2) is larger (at least half of the signal's max size)
# Peak detection :  Look at the gaps in between indices to identify where each peak begins and ends to find the midpoint
window = 21
der2 = signal.savgol_filter(signal_gyr_z, window_length=window, polyorder=2, deriv=2)
print(der2)
max_der2 = np.max(np.abs(der2))
print(max_der2)
large = np.where(np.abs(der2) > max_der2/2)[0]
print(large)
gaps = np.diff(large) > window
print(gaps)
begins = np.insert(large[1:][gaps], 0, large[0])
print(begins)
ends = np.append(large[:-1][gaps], large[-1])
print(ends)
peaks = ((begins+ends)/2).astype(np.int) 

# TODO: Zero-crossing
