import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

# Import csv
df1 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test1.csv')
df = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test2.csv')
df3 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test3.csv')
df4 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test4.csv')
df5 = pd.read_csv('/Users/parthvikulkarni/Capstone-1/Capstone/app/data/kick_test5.csv')

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
filt_gyr_z = signal.filtfilt(b, a, raw_gyr_z) # apply the filter

# Plot of IIR Filtered Data
plt.figure
plt.plot(time, filt_gyr_z, 'b')
plt.grid(True)
plt.show()

# Butterworth Filtered Data
# Example of how it should work
# Design an analog butterworth filter
b, a = signal.butter(4, 100, 'low', analog=True)
w, h = signal.freqs(b, a)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency
plt.show()

# Generate a signal made up of 10 Hz and 20 Hz, sampled at 1 kHz
t = np.linspace(0, 1, 1000, False)  # 1 second
sig = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*20*t)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 Hz and 20 Hz sinusoids')
ax1.axis([0, 1, -2, 2])

# Design a digital high-pass filter at 15 Hz to remove the 10 Hz tone, and apply it to the signal. (It's recommended to use second-order sections format when filtering, to avoid numerical error with transfer function (ba) format):
sos = signal.butter(10, 15, 'hp', fs=1000, output='sos')
filtered = signal.sosfilt(sos, sig) # apply the butterworth filter
ax2.plot(t, filtered)
ax2.set_title('After 15 Hz high-pass filter')
ax2.axis([0, 1, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

# Plot of Butterworth Filtered Data

