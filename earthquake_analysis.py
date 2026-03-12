import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 1. Fetch data from IRIS REST API
url = "http://service.iris.edu/irisws/timeseries/1/query"
params = {
    "net": "IU",
    "sta": "ANMO",
    "loc": "00",
    "cha": "BHZ",
    "starttime": "2020-07-22T06:12:44",
    "endtime": "2020-07-22T06:22:44",
    "output": "ascii1"  # Crucial: Returns plain text instead of binary data
}

print("Fetching data from IRIS...")
response = requests.get(url, params=params)
response.raise_for_status()

# 2. Parse the ASCII text response
lines = response.text.strip().split('\n')
data = []
sampling_rate = 40.0  # Safe default for BHZ channels

for line in lines:
    if line.startswith('TIMESERIES'):
        # Extract the exact sampling rate from the header (e.g., "... 40 sps ...")
        for part in line.split(','):
            if 'sps' in part:
                sampling_rate = float(part.replace('sps', '').strip())
    elif line and (line[0].isdigit() or line.startswith('-')):
        data.append(float(line))

data = np.array(data)
time_array = np.arange(len(data)) / sampling_rate

# 3. Preprocessing using SciPy
# Detrend (remove linear trend) and demean (remove constant mean)
data_detrended = signal.detrend(data, type='linear')
data_demeaned = signal.detrend(data_detrended, type='constant')

# Bandpass filter (0.1 to 10 Hz) using a Butterworth filter
nyquist = 0.5 * sampling_rate
low = 0.1 / nyquist
high = 10.0 / nyquist
b, a = signal.butter(4, [low, high], btype='bandpass')
data_filtered = signal.filtfilt(b, a, data_demeaned)



# 4. Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot the filtered waveform
ax1.plot(time_array, data_filtered, color='black', linewidth=0.5)
ax1.set_title("Filtered Waveform (0.1 - 10 Hz)")
ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Amplitude")

# Plot the spectrogram
ax2.specgram(
    data_filtered, 
    Fs=sampling_rate, 
    NFFT=256, 
    noverlap=128, 
    cmap='plasma'
)
ax2.set_title("Spectrogram")
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Frequency (Hz)")
ax2.set_ylim(0.1, 10)  # Match our bandpass filter range for visibility

plt.tight_layout()
plt.show()
