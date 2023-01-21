import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from numpy.fft import fft
import datetime

# Import csv
df = pd.read_csv('Capstone/app/data/testD.csv')

# Create Filter Parameters
b,a = signal.butter(4,0.1,'lowpass')

# Retrieve raw data files
raw_acc_x = df[df.columns[0]]
raw_acc_y = df[df.columns[1]]
raw_acc_z = df[df.columns[2]]
raw_gyr_x = df[df.columns[3]]
raw_gyr_y = df[df.columns[4]]
raw_gyr_z = df[df.columns[5]]