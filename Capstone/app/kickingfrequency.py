def zero_crossing(ms, zero_crossings):
    window_size = 1500
    length = len(ms)
    interval = ms[0] + window_size
    kicking_freq = []
    crossing = 0
    index = 0
    kicks = 0
    while(ms[length - 1] >= interval):
        while (ms[crossing] <= interval and index < len(zero_crossings[0])):
            crossing = zero_crossings[0][index]
            kicks = kicks + 1
            index = index + 1
        kicking_freq.append(kicks/(window_size/1000))
        kicks = 0
        interval = interval + window_size
    sum_frequency = 0
    num_windows = len(kicking_freq)
    for i in range(0, num_windows):
        sum_frequency = sum_frequency + kicking_freq[i]
    sum_frequency = sum_frequency * 2
    return sum_frequency/num_windows

def peak_detection(ms, numpeaks):
    window_size = 1500
    length = len(ms)
    interval = ms[0] + window_size
    kicking_freq = []
    peak = 0
    index = 0
    kicks = 0
    while(ms[length - 1] >= interval):
        while (ms[peak] <= interval and index < len(numpeaks[0])):
            peak = numpeaks[0][index]
            kicks = kicks + 1
            index = index + 1
        kicking_freq.append(kicks/(window_size/1000))
        kicks = 0
        interval = interval + window_size
    sum_frequency = 0
    num_windows = len(kicking_freq)
    for i in range(0, num_windows):
        sum_frequency = sum_frequency + kicking_freq[i]
    sum_frequency = sum_frequency * 2
    return sum_frequency/num_windows
