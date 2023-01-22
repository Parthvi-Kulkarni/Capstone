import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import signal
import datetime
import math
from ahrs.filters import Madgwick
from pyquaternion import Quaternion

# Import csv
df = pd.read_csv('C:/Users/jade-/PycharmProjects/Capstone/Capstone/app/data/testE.csv')

# Create Filter Parameters
b,a = signal.butter(4,0.1,'lowpass')

# Retrieve raw data files
raw_acc_x = df[df.columns[0]]/9.81
raw_acc_y = df[df.columns[1]]/9.81
raw_acc_z = df[df.columns[2]]/9.81
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

A = np.array([acc_x*9.81, acc_y*9.81, acc_z*9.81])
G = np.array([gyr_x*math.pi/180, gyr_y*math.pi/180, gyr_z*math.pi/180])
A = A.transpose()
G = G.transpose()

# Get time in seconds
seconds = []
start = datetime.datetime.strptime(time[0],'%H:%M:%S.%f')

for i in range(0,length):
    ts = datetime.datetime.strptime(time[i], '%H:%M:%S.%f')
    duration = ts - start
    sec = duration.total_seconds()
    seconds.append(sec)

# Get angle from gyroscope
ang_z = scipy.integrate.cumtrapz(gyr_z, seconds)
plt.plot(seconds[0:-1], ang_z)
plt.title('Rotation about Z over Time')
plt.xlabel('time (s)')
plt.ylabel('Angle (deg)')
plt.show()

# Combine Accelerometer and Gyroscope
madgwick = Madgwick()
Q = np.tile([1., 0., 0., 0.], (len(G),1))


for t in range(1, length):
    Q[t] = madgwick.updateIMU(Q[t - 1], gyr=G[t], acc=A[t])

print(Q.shape)

Quat = []
dist = []


for i in range (0,len(Q)):
    Quat.append(Quaternion(Q[i]))

for i in range(1,len(Q)):
    dist.append(Quaternion.distance(Quat[0], Quat[i]))

plt.plot(seconds[0:-1], dist)
plt.title('Quaternion distance over time')
plt.xlabel('time (s)')
plt.ylabel('distance (m)')
plt.show()

angle = []


for i in range(0,len(Quat)):
    angle.append(Quat[i].degrees)

plt.plot(seconds, angle)
plt.title('Quaternion angle over time')
plt.xlabel('time (s)')
plt.ylabel('angle (deg)')
plt.show()