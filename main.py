import sounddevice
import soundfile
import librosa
import numpy
from scipy.spatial import distance

# ALL CONSTANTS
sampleRate = 44100
duration = 1
recName = 'sound.wav'
numberOfMFCC = 15


def initialize():
    # gathered with the script calculate base sound!
    defaultSound = [-4.6976938e+02, 1.3127696e+02, 5.2812858e+00, - 2.8189064e+01,
                    4.0831825e+01, 1.6257446e+01, 2.2603125e+01, 2.3382446e+01,
                    3.0513359e+01, -2.4370581e+01, -5.4154949e+00, 1.1900447e+01,
                    1.9179310e+01, -1.3636537e+01, 1.7299581e+00, 7.9644477e-01,
                    -1.8546830e+00, -8.1769514e+00, 7.6307049e+00, -4.5180815e-01]
    calculate(defaultSound)


def calculate(defaultMfcc):
    print('Coffee project started...')

    # record sound of the environment and save in multi dimensional array
    # problems I got =>
    # 1) Blocking should be true!!
    # 2) Should be flattened otherwise the shape is 2 :)
    recording = sounddevice.rec(int(sampleRate * duration), samplerate=sampleRate, channels=2, blocking=True).flatten()

    # wait until array is done
    sounddevice.wait()

    # save soundfile to .wav file
    soundfile.write(recName, recording, sampleRate)

    # compute MFCC
    mfccResults = computeMeanMfcc(recording)
    print(mfccResults)

    # compute euclidian distance between 2 soundfiles
    score = calculateEuclidianDistance(mfccResults, defaultMfcc)
    print('The score is: ', score)


# function to compute the MFCC
# What is MFCC? =>
# all (Mel-frequency cepstral coefficients = MFCC) make up the (mel-frequency cepstrum (MFC))
# It is a representation of the short-term power spectrum of a sound
# Takes 4 arguments:
# 1) The array of sound
# 2) Sampling rate
# 3) Shape
# 4) Number of MFCC to get the MFC
def computeMeanMfcc(arraySound):
    mfcc = librosa.feature.mfcc(arraySound, sr=sampleRate, dtype='float32', n_mfcc=20)
    return numpy.mean(mfcc, axis=1)


def calculateEuclidianDistance(soundMFCC, default):
    return distance.euclidean(default, soundMFCC)


if __name__ == '__main__':
    initialize()
