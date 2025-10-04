# Import libraries
import obspy
from obspy import read, UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt

# Connect to IRIS client
client = Client("IRIS")

# Example earthquake: Alaska, 22 July 2020
event_time = UTCDateTime("2020-07-22T06:12:44")

# Download waveform data (station: IUANMO, channel: BHZ)
st = client.get_waveforms(network="IU", station="ANMO", location="00", channel="BHZ",
                          starttime=event_time, endtime=event_time + 600)

print(st)

# Preprocessing
st.detrend("linear")      # Remove linear trend
st.detrend("demean")      # Remove mean
st.filter("bandpass", freqmin=0.1, freqmax=10)   # Apply bandpass filter

# Plot processed waveform
st.plot()

# Spectrogram
tr = st[0]
tr.spectrogram(log=True, wlen=50, cmap="plasma")
plt.show()
