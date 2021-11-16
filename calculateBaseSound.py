import sounddevice
import librosa
import numpy

# ALL CONSTANTS
sampleRate = 44100
duration = 1
recName = 'sound.wav'
numberOfMFCC = 15

def initialize():
    print('start sound')
    recording = sounddevice.rec(int(sampleRate * duration), samplerate=sampleRate, channels=2, blocking=True).flatten()

    # wait until array is done
    sounddevice.wait()

    # compute MFCC
    mfccResults = computeMeanMfcc(recording)
    print(mfccResults)

def computeMeanMfcc(arraySound):
    mfcc = librosa.feature.mfcc(arraySound, sr=sampleRate, dtype='float32', n_mfcc=20)
    return numpy.mean(mfcc, axis=1)

if __name__ == '__main__':
    initialize()
