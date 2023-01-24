import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from numpy.fft import fft
import kickingfrequency

# Import csv
df = pd.read_csv('Capstone/app/data/swim1.csv')

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

seconds = []
for i in range(0,length):
    second = time[i]/1000000
    seconds.append(second)

# Add a column to the dataframe
len(seconds)

plt.title('Raw Angular Velocity in the Z Direction')
plt.xlabel('Time')
plt.ylabel('Raw Angular Velocity')
plt.plot(seconds, raw_gyr_z, 'b')
plt.show()

# Create Filter Parameters
b,a = signal.butter(4,0.1,'lowpass')

# Filter Signals
acc_x = signal.filtfilt(b, a, raw_acc_x)
acc_y = signal.filtfilt(b, a, raw_acc_y)
acc_z = signal.filtfilt(b, a, raw_acc_z)
gyr_x = signal.filtfilt(b, a, raw_gyr_x)
gyr_y = signal.filtfilt(b, a, raw_gyr_y)
gyr_z = signal.filtfilt(b, a, raw_gyr_z)

plt.title('Raw Angular Velocity in the Z Direction')
plt.xlabel('Time')
plt.ylabel('Raw Angular Velocity')
plt.plot(time, raw_gyr_z, 'b')
plt.show()

FFT = fft(raw_gyr_z)
N = len(FFT)
sample_frequency = 88
freq = np.linspace(0, sample_frequency, N)
plt.title('FFT Spectrum of Angular Velocity in the Z Direction')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count')
plt.xlim(0, sample_frequency/2)
plt.plot(freq, FFT)
plt.show()

b, a = signal.butter(3, 0.0175, 'low') # 3 order of the filter and 0.05 would be the highpass cutoff
signal_gyr_z = signal.filtfilt(b, a, raw_gyr_z) # apply the filter



# Zero-crossing
zero_crossings = np.where(np.diff(np.signbit(signal_gyr_z)))
zeros = np.zeros(len(zero_crossings))

plt.title('Gyroscope Data in the Z direction')
plt.xlabel('Time')
plt.ylabel('Angular Velocity')
plt.xlim(156489203, 231489294)
plt.plot(time, signal_gyr_z, 'b')
plt.plot(zero_crossings, zeros, marker='o')
plt.show()
# milliseconds = []


# for i in range(0,length):
#     timestamp = datetime.datetime.strptime(time[i], '%H:%M:%S.%f')
#     ms = timestamp.timestamp() * 1000
#     milliseconds.append(ms)

# Add a column to the dataframe
# df['Milliseconds'] = milliseconds

# ms = df[df.columns[8]]
average_frequency = kickingfrequency.zero_crossing(time, zero_crossings)
print('Kicking frequency: ' + str(average_frequency) + ' kicks per second')
