import sounddevice as sd
import numpy as np
import pika
import time
import scipy
import sys
import os
from time import sleep

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='servo')
    channel.queue_declare(queue='audio_output')
    # channel.queue_declare(queue='audio_input')
    
    def threshold_met():
        channel.basic_publish(exchange='', routing_key='servo', body='demo')
        channel.basic_publish(exchange='', routing_key='audio_output', body='demo')
        
    frequency_threshold = 1200
    while True:
        data = sd.rec(1024, 44100, channels=2, blocking=True)
        frequencies, times, spectrogram = scipy.signal.stft(data[:, 0], 44100, nperseg=1024)
        max_frequency = np.abs(frequencies[np.argmax(spectrogram)])
        print("Frequency: " + str(max_frequency))
        if max_frequency > frequency_threshold:
            threshold_met()
            time.sleep(40)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
