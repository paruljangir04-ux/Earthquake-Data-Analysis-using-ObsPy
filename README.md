# Earthquake-Data-Analysis-using-ObsPy
A beginner-friendly project demonstrating how to download, preprocess, and visualize real earthquake waveform data using ObsPy. Includes seismogram and spectrogram plots, making it a simple introduction to seismological data analysis.
# Earthquake Data Analysis and Visualization using ObsPy

##  Aim
To download real earthquake waveform data using ObsPy, process it, and visualize both the time-series seismogram and spectrogram.

---

##  Introduction
Seismology is the study of seismic waves that travel through the Earth.  
In this project, we use **ObsPy**, a Python toolbox for seismology, to:
- Fetch earthquake data from public seismic networks.
- Preprocess the data (detrending, filtering).
- Plot the waveform and spectrogram.

This project demonstrates how seismologists handle real seismic data, and it is useful as a starter project for internships.

---

##  Methodology
1. **Data Collection**  
   - Connect to IRIS server using ObsPy client.  
   - Fetch earthquake waveform data for a chosen station.  

2. **Preprocessing**  
   - Remove linear trends and mean.  
   - Apply a bandpass filter (0.1–10 Hz).  

3. **Analysis**  
   - Plot the seismogram.  
   - Generate and visualize the spectrogram.  

4. **Conclusion**  
   - Basic waveform analysis and visualization achieved.
  
   - #  Import libraries
import obspy
from obspy import read, UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt
#  Connect to IRIS client
client = Client("IRIS")

# Example earthquake: Alaska, 22 July 2020
event_time = UTCDateTime("2020-07-22T06:12:44")

#  Download waveform data (station: IUANMO, channel: BHZ)
st = client.get_waveforms(network="IU", station="ANMO", location="00", channel="BHZ",
                          starttime=event_time, endtime=event_time + 600)

print(st)

#  Preprocessing
st.detrend("linear")      # Remove linear trend
st.detrend("demean")      # Remove mean
st.filter("bandpass", freqmin=0.1, freqmax=10)   # Apply bandpass filter

# Plot processed waveform
st.plot()

# Spectrogram
tr = st[0]
tr.spectrogram(log=True, wlen=50, cmap="plasma")
plt.show()

---

##  Conclusion
- Successfully downloaded seismic waveform data using ObsPy.  
- Preprocessed with detrending and bandpass filtering.  
- Visualized both the **seismogram** and **spectrogram**.  

This project demonstrates the basic workflow in seismology data analysis.  
Future improvements may include:
- Automatic phase picking (P and S waves).  
- Comparing waveforms across multiple stations.  
- Computing travel-time curves.  

---

## Project Structure

### `README.md`
```markdown
# Earthquake Data Analysis using ObsPy

This repository demonstrates how to:
- Fetch earthquake waveform data from IRIS.
- Preprocess and filter data.
- Plot seismograms and spectrograms.

## How to Run
1. Clone this repo  
2. Install requirements: `pip install -r requirements.txt`  
3. Open Jupyter Notebook and run `earthquake_analysis.ipynb`


