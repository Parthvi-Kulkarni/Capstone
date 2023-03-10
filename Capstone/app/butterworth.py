import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

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
sos = signal.butter(10, 15, 'hp', fs=2463, output='sos')
filtered = signal.sosfilt(sos, sig) # apply the butterworth filter
ax2.plot(t, filtered)
ax2.set_title('After 15 Hz high-pass filter')
ax2.axis([0, 1, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

