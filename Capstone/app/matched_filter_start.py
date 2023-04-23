from scipy.signal import correlate
import math 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt



def start_time(df):
    sig = df['raw_gyr_z']
    sig_template = pd.read_csv('template.csv')
    sig_template = sig_template.astype(str)
    sig_template.str.pad(sig,fillchar='0')
    corr = correlate(sig_template,sig, mode='full') / len(sig)

    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
    ax_orig.plot(sig)
    ax_orig.set_title('Original signal')
    ax_noise.plot(sig_template)
    ax_noise.set_title('Signal with noise')
    ax_corr.plot(corr)
    ax_corr.axhline(0.5, ls=':')
    ax_corr.set_title('Cross-correlated')
    ax_orig.margins(0, 0.1)
    fig.tight_layout()
    plt.show()
    
df = pd.read_csv('/')
start_time(df)