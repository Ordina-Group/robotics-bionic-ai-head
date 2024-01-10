import sounddevice as sd
import numpy as np
import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='audio_input')
    
    def threshold_met():
        channel.basic_publish(exchange='', routing_key='audio_input', body='Audio detected')
        
    frequency_threshold = 1000
    while True:
        data = sd.rec(1024, 44100, channels=2)
        frequencies, times, spectrogram = stft(data, 44100, nperseg=1024)
        max_frequency = np.abs(frequencies[np.argmax(spectrogram)])
        if max_frequency > frequency_threshold:
            threshold_met()
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
