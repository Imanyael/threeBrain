# Context

## CONTAINED OBJECTS

There can only be one type of raw data in a BRW-file at any time. Thus, it will always contain either
Raw, WaveletBasedRaw or EventBasedSparseRaw dataset, and the corresponding TOC dataset.
• Raw: a 1-dimensional dataset of Bytes containing recorded data when no compression is
applied.

• RawTOC: a 1-dimensional dataset of 64-bit Integers containing the position inside the Raw
dataset of the first raw value recorded for each data chunk when no compression is applied.

• WaveletBasedEncodedRaw: a 1-dimensional dataset of 16-bit Integers containing recorded
data when wavelet compression is applied.

• WaveletBasedEncodedRawTOC: a 1-dimensional dataset of 64-bit Integers containing the
position inside the WaveletBasedEncodedRaw of the first compressed value recorded for each
data chunk when wavelet compression is applied. It has two 32-bit Integer attributes
CompressionLevel and DataChunkLength, where the former indicates the amount of
compression applied, and the latter indicates the number of samples represented by the
coefficients in each chunk.

• EventsBasedSparseRaw: a 1-dimensional dataset of Bytes containing recorded data when
events-based compression (currently, this compression corresponds to the Noise Blanking
compression; see also BrainWave 5 user guide) is applied.

3Brain - File Format Documentation For BRW v4.x, BXR v3.x and BCMP v1.x 13 of 23
• EventsBasedSparseRawTOC: a 1-dimensional dataset of 64-bit Integers containing the
position inside the EventsBasedSparseRaw dataset of the first compressed value recorded for
each data chunk when events-based compression is applied.

• NoiseMean: a 1-dimensional dataset of 32-bit floating-point values containing the measured
mean values for each channel and for each data chunk. Values are referred to digital sample
values that need to be converted to analog values.

• NoiseStdDev: a 1-dimensional dataset of 32-bit floating-point values containing the
measured standard deviation values for each channel and for each data chunk. Values are
referred to digital sample values that need to be converted to analog values.

• NoiseTOC: a 1-dimensional dataset of 64-bit Integers containing the position inside noise related
datasets (e.g., NoiseMean NoiseStdDev) of the first noise value recorded for each data
chunk.

##
• NoiseChIdxs: a 1-dimensional dataset of 32-bit Integers containing the linear indexes of all
channels whose noise values have been considered valid. During recording, some channels
showing noise values outside the normal distribution might be considered outliers and
ignored for the analysis.

• StoredChIdxs: a 1-dimensional dataset of 32-bit Integers containing the linear indexes of all
BioSPU-chip channels that have been recorded.

## RAW
The Raw dataset can contain either one single Recording Interval (possibly divided into multiple
contiguous data chunks) or multiple Recording Intervals. In the latter case, the recorded intervals
are saved from the stream coming from the CEI Plate according to the recording conditions, like
for instance user-defined intervals, or protocol-defined intervals.
The Raw array consists of a series of Bytes that define all the frames inside the data chunks. A
frame is indivisible and cannot be partially recorded. As illustrated in the following picture, for
each data chunk a range of values is stored. The beginning of each chunk is identified by FS(i)
that is stored in the Root TOC and represents the starting frame number of the chunk, and by
DP_K(i) that is stored in the RawTOC and marks the position in number of elements (in this case
Bytes) inside the Raw dataset.
Each range consists of M x S values, where M is the number of channels recorded, and S is the
number of samples (frames) per chunk per channel. Each sample is encoded in digital values and
converted into the corresponding analogue value (see Samples).

## BRX File

Each kind of event recorded by Brainwave is defined by a set of properties. For example, a spike
can be defined through the time at which it was recorded, the channel it was recorded on, and its
waveform. This information is split over multiple datasets, one for each property, but all datasets
share the same number of elements so that a given event is defined by all the properties found at
the same position in the corresponding datasets.
For each type of event a TOC is also defined, which indicates for each recorded data chunk the
position of the first event recorded.
Here the list of all available datasets:

##
• SpikeChIdxs: a 1-dimensional array of 32-bit Integers, representing for each detected spike
the linear index of the channel it has been recorded on.

• SpikeForms: a 1-dimensional array of 16-bit Integers of length M = N x W, where N is the
number of spikes detected, and W is the number of frames stored for each waveform. It
3Brain - File Format Documentation For BRW v4.x, BXR v3.x and BCMP v1.x 21 of 23
contains the waveforms for each detected spike, collapsed into one dimension. It has a 32-bit
Integer attribute Wavelength indicating the length, in frames, of the waveforms (W). From
Root Version 301, it has a 32-bit Integer attribute WaveTimeOffset indicating the position, in
frames, of the detected peak in the wave, which corresponds to the action potential’s peak.
To get the position of the waveform (event’s property) of a given spike, the value found in
SpikeTOC must be multiplied by W.

• SpikeTOC: a 1-dimensional array of 64-bit Integers, containing the position inside spike
datasets (e.g., SpikeChIdxs, SpikeTimes) of the first spike detected for each data chunk.

• SpikeTimes: a 1-dimensional array of 64-bit Integers, representing the time instant, in
number of frames, in which each spike has been detected.

• SpikeUnits: a 1-dimensional array of 32-bit Integers, representing the Unit Identifier for each
detected spike. It is defined only if Spike Sorting has been performed.

• SpikeBurstChIdxs: a 1-dimensional array of 32-bit Integers, representing for each detected
spike burst the linear index of the channel it has been recorded on.

• SpikeBurstTOC: a 1-dimensional array of 64-bit Integers, containing the position inside spike
burst datasets (e.g., SpikeBurstChIdxs, SpikeBurstTimes) of the first spike burst detected
for each data chunk.

• SpikeBurstTimes: a 1-dimensional array of 64-bit Integers, representing the time instant, in
frames, in which each spike burst has been detected.

• SpikeBurstUnits: a 1-dimensional array of 32-bit Integers, representing the Unit Identifier
for each detected spike burst. It is defined only if Spike Sorting has been performed.

• SpikeNetworkBurstTOC: a 1-dimensional array of 64-bit Integers, containing the position
inside spike network burst datasets (e.g., SpikeNetworkBurstChIdxs,
SpikeNetworkBurstTimes) of the first spike network burst detected for each data chunk.

• SpikeNetworkBurstTimes: a 1-dimensional array of 64-bit Integers, representing the time
instant, in frames, in which each spike network burst has been detected.

• FpChIdxs: a 1-dimensional array of 32-bit Integers, representing for each detected field
potential the linear index of the channel it has been recorded on.

• FpForms: a 1-dimensional array of 16-bit Integers of length M = N x W, where N is the number
of field potentials detected, and W is the number of frames stored for each waveform. It
contains the waveforms for each detected field potential, collapsed into one dimension. It
has a 32-bit Integer attribute Wavelength indicating the length, in frames, of the waveforms
(W). As field potentials can have different waveform length, waves shorter than Wavelength
frames are 0-padded. To get the position of the waveform (event’s property) of a given field
potential, the value found in FpTOC must be multiplied by W.

• FpTOC: a 1-dimensional array of 64-bit Integers, containing the position inside field potential
datasets (e.g., FpChIdxs, FpTimes) of the first field potential detected for each data chunk.

• FpTimes: a 1-dimensional array of 64-bit Integers, representing the time instant, in frames, in
which each field potential has been detected.

• FpBurstChIdxs: a 1-dimensional array of 32-bit Integer values, representing for each
detected field potential burst the linear index of the channel it has been recorded on.
3Brain - File Format Documentation For BRW v4.x, BXR v3.x and BCMP v1.x 22 of 23

• FpBurstTOC: a 1-dimensional array of 64-bit Integer values, representing the position inside
field potential burst datasets (e.g., FpBurstChIdxs, FpBurstTimes) of the first field potential
burst event type at the beginning of each data.

• FpBurstTimes: a 1-dimensional array of 64-bit Integers, representing the time instant, in
frames, in which each field potential burst has been detected.

• FpNetworkBurstTOC: a 1-dimensional array of 64-bit Integers, containing the position inside
field potential network burst datasets (FpNetworkBurstChIdxs, FpNetworkBurstTimes) of
the first field potential network burst detected for each data chunk.

• FpNetworkBurstTimes: a 1-dimensional array of 64-bit Integers, representing the time
instant, in frames, in which each field potential network burst has been recorded.

• CfpTOC: a 1-dimensional array of 64-bit Integers, containing the position inside cardiac field
potential datasets (e.g., CfpChIdxs, CfpTimes) of the first cardiac field potential detected for
each data chunk.

• CfpTimes: a 4-dimensional array of 64-bit Integers, representing the time instants, in frames,
of the Q, R, S and T points of each detected cardiac field potential. A value of -1 means that it
was not possible to detect such point for that event.

• CfpChIdxs: a 1-dimensional array of 32-bit Integer values, representing for each detected
cardiac field potentials the linear index of the channel it has been recorded on.

• CfpForms: a 1-dimensional array of 16-bit Integers of length M = N x W, where N is the
number of cardiac field potentials detected, and W is the number of frames stored for each
waveform. It contains the waveforms for each detected field potential, collapsed into one
dimension. It has a 32-bit Integer attribute Wavelength indicating the length, in frames, of the
waveforms (W). It also has a 32-bit Integer attribute WaveTimeOffset indicating the position,
in frames, of the detected peak in the wave, which corresponds to R if positive threshold has
been used, S otherwise. To get the position of the waveform (event’s property) of a given
cardiac field potential, the value found in CfpTOC must be multiplied by W.
