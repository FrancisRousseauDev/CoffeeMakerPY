import sounddevice
import soundfile
import librosa
import numpy
from scipy.spatial import distance
import psycopg2
from credential import credentials
from apscheduler.schedulers.blocking import BlockingScheduler
import dash
from layout.index import showHTML

# ALL CONSTANTS
sampleRate = 44100
duration = 1
recName = 'sound.wav'
numberOfMFCC = 15
threshold = 90

app = dash.Dash(__name__)


def initialize():
    # gathered with the script calculate base sound!
    defaultSound = [-6.9496429e+02, 1.3378967e+02, 2.8810219e+01, -6.0626235e+00,
                    2.5864054e+01, 1.5894449e+00, -1.2138181e+00, 8.8368406e+00,
                    2.1701456e+01, -1.2967456e+01, -9.4427032e+00, 2.1754055e+00,
                    1.2950614e+01, -2.6109576e+00, 5.0735421e+00, 1.4910783e+00,
                    6.9868284e-01, -2.3935324e-01, 1.0540934e+01, 8.1045091e-01]

    coffeeSound = [-510.12238, 205.94772, 16.054848, -37.645023, 60.11539,
                   -12.5140505, -12.873933, -1.4891857, 39.331104, -33.3275,
                   -5.371215, 3.1046267, 12.120397, -23.374199, 13.742373,
                   4.42839, -7.2044516, -10.38817, 15.771467, 0.5177491]
    calculate(defaultSound)


def calculate(defaultMfcc):
    print('Listening for a coffee machine...')

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

    # compute euclidian distance between 2 soundfiles
    score = calculateEuclidianDistance(mfccResults, defaultMfcc)

    if score < threshold:
        addRowToDatabase(score)
    else:
        print('sound doesnt match to the coffee machine: (', score, ')')


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


# matching-two-series-of-mfcc-coefficients is the easiest to do with this, believe me :)
# it calculates the length of a line segment between the two points
def calculateEuclidianDistance(soundMFCC, default):
    return distance.euclidean(default, soundMFCC)


def addRowToDatabase(score):
    try:
        connection = psycopg2.connect(user=credentials.user,
                                      password=credentials.password,
                                      host=credentials.host,
                                      port=credentials.port,
                                      database=credentials.database)
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO public.consumption ("coffeeID", "score") VALUES (%s, %s)"""
        record_to_insert = ("2", score)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table consumption (", score, ")")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table consumption: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':

    # ADD SCHEDULER
    sched = BlockingScheduler()
    sched.add_job(initialize, 'interval', seconds=2)

    try:
        sched.start()
        showHTML(app)
        # RUN THE layout BY DASH
        app.run_server(debug=True)
    except (KeyboardInterrupt, SystemExit):
        pass
