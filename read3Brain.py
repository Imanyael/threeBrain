import numpy as np
import matplotlib.pyplot as plt
import h5py
#
#  variables

def DecodeEventBasedRawData(file, data, wellID, startFrame, numFrames):
# collect the TOCs
    toc = np.array(file['TOC'])
    eventsToc = np.array(file[wellID + '/EventsBasedSparseRawTOC'])
    # from the given start position and duration in frames, localize the corresponding event positions
    # using the TOC
    tocStartIdx = np.searchsorted(toc[:, 1], startFrame)
    tocEndIdx = min(np.searchsorted(toc[:, 1], startFrame + numFrames, side='right')
    + 1, len(toc) - 1)
    eventsStartPosition = eventsToc[tocStartIdx]
    eventsEndPosition = eventsToc[tocEndIdx]
    # decode all data for the given well ID and time interval
    binaryData = file[wellID + '/EventsBasedSparseRaw'][eventsStartPosition:eventsEndPosition]
    binaryDataLength = len(binaryData)
    pos = 0
    while pos < binaryDataLength:
        chIdx = int.from_bytes(binaryData[pos:pos + 4], byteorder='little', signed=True)
        pos += 4
        chDataLength = int.from_bytes(binaryData[pos:pos + 4], byteorder='little', signed=True)
        pos += 4
        chDataPos = pos
    while pos < chDataPos + chDataLength:
        fromInclusive = int.from_bytes(binaryData[pos:pos + 8], byteorder='little', signed=True)
        pos += 8
        toExclusive = int.from_bytes(binaryData[pos:pos + 8], byteorder='little', signed=True)
        pos += 8
        rangeDataPos = pos
        for j in range(fromInclusive, toExclusive):
            if j >= startFrame + numFrames:
                break
            if j >= startFrame:
                data[chIdx][j - startFrame] = int.from_bytes(
                binaryData[rangeDataPos:rangeDataPos + 2], byteorder='little', signed=True)
                rangeDataPos += 2
                pos += (toExclusive - fromInclusive) * 2

def GenerateSyntheticNoise(file, data, wellID, startFrame, numFrames):
    # collect the TOCs
    toc = np.array(file['TOC'])
    noiseToc = np.array(file[wellID + '/NoiseTOC'])
    # from the given start position in frames, localize the corresponding noise positions
    # using the TOC
    tocStartIdx = np.searchsorted(toc[:, 1], startFrame)
    noiseStartPosition = noiseToc[tocStartIdx]
    noiseEndPosition = noiseStartPosition
    for i in range(tocStartIdx + 1, len(noiseToc)):
        nextPosition = noiseToc[i]
        if nextPosition > noiseStartPosition:
            noiseEndPosition = nextPosition
            break
    if noiseEndPosition == noiseStartPosition:
        for i in range(tocStartIdx - 1, 0, -1):
            previousPosition = noiseToc[i]
            if previousPosition < noiseStartPosition:
                noiseEndPosition = noiseStartPosition
                noiseStartPosition = previousPosition
                break
    # obtain the noise info at the start position
    noiseChIdxs = file[wellID + '/NoiseChIdxs'][noiseStartPosition:noiseEndPosition]
    noiseMean = file[wellID + '/NoiseMean'][noiseStartPosition:noiseEndPosition]
    noiseStdDev = file[wellID + '/NoiseStdDev'][noiseStartPosition:noiseEndPosition]
    noiseLength = noiseEndPosition - noiseStartPosition
    noiseInfo = {}
    meanCollection = []
    stdDevCollection = []

    for i in range(1, noiseLength):
        noiseInfo[noiseChIdxs[i]] = [noiseMean[i], noiseStdDev[i]]
        meanCollection.append(noiseMean[i])
        stdDevCollection.append(noiseStdDev[i])
        # calculate the median mean and standard deviation of all channels to be used for
        # invalid channels
        dataMean = np.median(meanCollection)
        dataStdDev = np.median(stdDevCollection)
    # fill with Gaussian noise
    for chIdx in data:
        if chIdx in noiseInfo:
            data[chIdx] = np.array(np.random.normal(noiseInfo[chIdx][0], noiseInfo[chIdx][1],
            numFrames), dtype=np.int16)
        else:
            data[chIdx] = np.array(np.random.normal(dataMean, dataStdDev, numFrames),
            dtype=np.int16)

# main
fileDirectory = r'C:\Development\threeBrain'
# fileName = 'testFile.brw'
fileName = r'\NewPhase_3D_1min.brw'
wellID = 'Well_A1'
useSyntheticNoise = True
dataStartPositionSec = 0
dataDurationSec = 3
# open the BRW file
file = h5py.File(fileDirectory + fileName, 'r')
# collect experiment information
samplingRate = file.attrs['SamplingRate']
chIdxs = np.array(file[wellID + '/StoredChIdxs'])
# convert the requested time interval from seconds to frames
startFrame = int(dataStartPositionSec * samplingRate)
numFrames = int(dataDurationSec * samplingRate)
# initialize an empty (fill with zeros) data collection
data = {}
for chIdx in chIdxs:
    data[chIdx] = np.zeros(numFrames, dtype=np.int16)

# fill the data collection with Gaussian noise if requested
if useSyntheticNoise:
    GenerateSyntheticNoise(file, data, wellID, startFrame, numFrames)
    # fill the data collection with the decoded event based sparse raw data
    DecodeEventBasedRawData(file, data, wellID, startFrame, numFrames)
# close the file
file.close()
# visualize the decoded raw signal from the first channel
x = np.arange(startFrame, startFrame + numFrames, 1) / samplingRate
y = np.fromiter(data[chIdxs[0]], float)
plt.figure()
plt.plot(x, y, color="blue")
plt.title('Raw Signal')
plt.xlabel('(sec)')
plt.ylabel('(ADC Count)')
plt.show()