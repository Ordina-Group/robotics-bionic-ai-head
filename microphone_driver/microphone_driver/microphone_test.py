import sounddevice as sd
import numpy as np
import scipy
import sys
import os
from time import sleep

def main():
    def threshold_met():
        print('Threshold met!')

    frequency_threshold = 2000
    while True:
        data = sd.rec(1024, 44100, channels=2, blocking=True)
        frequencies, times, spectrogram = scipy.signal.stft(data[:, 0], 44100, nperseg=1024)
        max_frequency = np.abs(frequencies[np.argmax(spectrogram)])
        print("Frequency: " + str(max_frequency))
        if max_frequency > frequency_threshold:
            threshold_met()
            print("Frequency")
            sleep(1)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
