from shutil import which

import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd
import scipy
from scipy import signal
import datetime
import math
from ahrs.filters import Madgwick
from pyquaternion import Quaternion

# Import csv
from Capstone.app.IFFT import fourierFilt

df = pd.read_csv("C:/Users/jade-/OneDrive/Documents/UBC 2022-23/BMEG 457/Testing/February 2023/Feb22.csv")

# Retrieve raw data files
raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_gyr_z = df[df.columns[5]]
length = len(raw_gyr_z)
raw_acc_z = numpy.zeros(length)
raw_gyr_x = numpy.zeros(length)
raw_gyr_y = numpy.zeros(length)

time = df[df.columns[7]]
seconds = []

for i in range(0, length):
    seconds.append(time[i]/math.pow(10, 6) - time[0]/math.pow(10, 6))

seconds.append(seconds[-2]+seconds[-2]-seconds[-3])

raw_A = np.array([raw_acc_x, raw_acc_y, raw_acc_z])
raw_G = np.array([raw_gyr_x*math.pi/180, raw_gyr_y*math.pi/180, raw_gyr_z*math.pi/180])

raw_A = raw_A.transpose()
raw_G = raw_G.transpose()

madgwick_init = Madgwick()
Q_init = np.tile([1., 0., 0., 0.], (length,1))

for t in range(1, length):
    Q_init[t] = madgwick_init.updateIMU(Q_init[t - 1], gyr=raw_G[t], acc=raw_A[t])

print(Q_init.shape)

Quat = []
distRad = []
distDeg = []

distRad.append(0)

for i in range(0, len(Q_init)):
    Quat.append(Quaternion(Q_init[i]))

for i in range(1, len(Q_init)):
    distRad.append(Quaternion.distance(Quat[i-1], Quat[i]))

for i in range(0, len(distRad)):
    distDeg.append(distRad[i]*180/math.pi)

plt.plot(distDeg)
plt.title('Quaternion angle over time')
plt.xlabel('time (s)')
plt.ylabel('angle (deg)')
plt.show()

b,a = signal.butter(4,0.1,'lowpass')

window_size = 88
numbers_series = pd.Series(signal.filtfilt(b,a,distDeg))
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages = np.array(moving_averages.tolist())

thresh = 0.5
greater = np.where(moving_averages>thresh, 1, moving_averages)
greater[greater <= thresh] = 0
greater[greater == numpy.nan] = 0
first = np.where(greater == 1)[0][0] - 100
last = np.where(greater == 1)[0][-1] + 100
print(first)
print(last)

length = last-first

fft_acc_x = fourierFilt(np.array(raw_acc_x[first:last]))
fft_acc_y = fourierFilt(np.array(raw_acc_y[first:last]))
fft_gyr_z = fourierFilt(np.array(raw_gyr_z[first:last]))

acc_x = signal.filtfilt(b, a, fft_acc_x)
acc_y = signal.filtfilt(b, a, fft_acc_y)
gyr_z = signal.filtfilt(b, a, fft_gyr_z)

acc_z = np.zeros(len(acc_x))
gyr_x = np.zeros(len(acc_x))
gyr_y = np.zeros(len(acc_x))

seconds = seconds[first+1:last]

A = np.array([acc_x, acc_y, acc_z])
G = np.array([gyr_x*math.pi/180, gyr_y*math.pi/180, gyr_z*math.pi/180])

A = A.transpose()
G = G.transpose()

madgwick = Madgwick()
Q = np.tile([1., 0., 0., 0.], (length,1))

for t in range(1, length):
    Q[t] = madgwick.updateIMU(Q[t - 1], gyr=G[t], acc=A[t])

print(Q.shape)

Quat = []
distRad = []
distDeg = []

for i in range(0, len(Q)):
    Quat.append(Quaternion(Q[i]))

for i in range(1, len(Q)):
    distRad.append(Quaternion.distance(Quat[i-1], Quat[i]))

for i in range(0, len(distRad)):
    distDeg.append(distRad[i]*180/math.pi)

plt.plot(seconds, distDeg)
plt.title('Quaternion angle over time')
plt.xlabel('time (s)')
plt.ylabel('angle (deg)')
plt.show()