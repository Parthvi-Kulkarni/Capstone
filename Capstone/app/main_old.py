from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from numpy.fft import fft
import kickingfrequency
import math

# Import csv
df = pd.read_csv('')

raw_acc_x = df[df.columns[0]]/9.81
raw_acc_y = df[df.columns[1]]/9.81
raw_acc_z = df[df.columns[2]]/9.81
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]

raw_A1 = [raw_acc_x, raw_acc_y, raw_acc_z]
raw_G1 = [raw_gyr_x, raw_gyr_y, raw_gyr_z]

time = df[df.columns[7]]
length = len(time)

# Convert microseconds to seconds
seconds = []
for i in range(0, length):
    seconds.append(time[i]/math.pow(10, 6))

## To handle timestamping for datasets D, E, and F:
# milliseconds = []
# for i in range(0,length):
#     timestamp = datetime.strptime(time[i], '%H:%M:%S.%f')
#     ms = timestamp.timestamp() * 1000
#     milliseconds.append(ms)
# df['Milliseconds'] = milliseconds
# ms = df[df.columns[8]]

# Visualization of Raw Data
plt.plot(time, raw_gyr_z, color='b', label='Noisy Signal')
plt.xlabel('Time (seconds)')
plt.ylabel('Angular Velocity')
plt.show()

# Compute Fourier Transform
fs = 100
dt = 1/fs
n = length
fhat = np.fft.fft(raw_gyr_z, n) #computes the fft
psd = fhat * np.conj(fhat)/n
freq = (1/(dt*n)) * np.arange(n) #frequency array
idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index

# Visualization of Fourier Transform
plt.plot(freq[idxs_half], np.abs(psd[idxs_half]), color='b', lw=0.5, label='PSD noisy')
plt.xlabel('Frequencies in Hz')
plt.ylabel('Amplitude')
plt.show()

# INSERT IFFT HERE
#
#


b,a = signal.butter(4,3.14/fs,'lowpass')
signal_filtered = signal.filtfilt(b, a, raw_gyr_z)

# Filter Signals
acc_x = signal.filtfilt(b, a, raw_acc_x)
acc_y = signal.filtfilt(b, a, raw_acc_y)
acc_z = signal.filtfilt(b, a, raw_acc_z)
gyr_x = signal.filtfilt(b, a, raw_gyr_x)
gyr_y = signal.filtfilt(b, a, raw_gyr_y)

#Visualization
fig, ax = plt.subplots(2,1)
ax[0].plot(seconds, raw_gyr_z, color='b', lw=0.5, label='Noisy Signal')
ax[0].set_xlabel('Time (seconds)')
ax[0].set_ylabel('Angular Velocity')
ax[0].legend()

ax[1].plot(seconds, signal_filtered, color='r', lw=1, label='Clean Signal Retrieved')
ax[1].set_xlabel('Time (seconds)')
ax[1].set_ylabel('Angular Velocity')
ax[1].legend()

plt.subplots_adjust(hspace=0.4)
plt.show()

plt.plot(seconds, raw_gyr_z, color='b', label="Noisy Signal")
plt.plot(seconds, signal_filtered, color='r', label="Clean Signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Angular Velocity")
plt.show()

fhat2 = np.fft.fft(signal_filtered, n) #computes the fft
psd_clean = fhat2 * np.conj(fhat2)/n

plt.plot(freq[idxs_half], np.abs(psd_clean[idxs_half]), color='b', lw=0.5, label='PSD clean')
plt.xlabel('Frequencies in Hz')
plt.ylabel('Amplitude')
plt.show()

# Zero-crossing
zero_crossings = np.where(np.diff(np.signbit(signal_filtered)))
zeros = np.zeros(len(zero_crossings))

length = len(seconds)
translated_time = []
for i in range(0, length):
    translated_time.append(seconds[i] - seconds[0])

# plt.title('Gyroscope Data')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Angular Velocity')
# plt.plot(seconds, signal_filtered, 'b')
# plt.plot(zero_crossings, zeros, marker='o')
# plt.show()


## IMPLEMENT NEW ZERO_CROSSING METHOD HERE INSTEAD OF CALLING KICKING FREQUENCY
average_frequency = kickingfrequency.zero_crossing(time, zero_crossings)
print('Kicking frequency: ' + str(average_frequency) + ' kicks per second')