import os
import pika
import sys
import sounddevice as sd
import soundfile as sf
import numpy
import time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='audio_output')
    
    # TODO - specify audio file path
    audio_file_path1 = 'melvinintro.wav'
    audio_file_path2 = 'hahaha.wav'
    
    def callback(ch, method, properties, body):
        instructions = body.decode().split(':')
        if instructions[0] == 'play_sound':
            audio_data, fs = sf.read(audio_file_path, dtype='float32')
            sd.play(audio_data, fs)
            sd.wait()
        elif instructions[0] == 'demo':
            time.sleep(4)
            audio_data, fs = sf.read(audio_file_path1, dtype='float32')
            sd.play(audio_data, fs)
            sd.wait()
        elif instructions[0] == 'laugh':
            time.sleep(0.3)
            audio_data, fs = sf.read(audio_file_path2, dtype='float32')
            sd.play(audio_data, fs)
            sd.wait()
        elif instructions[0] == 'speak':
	        print("speak")
            # Add functionality to generate text-to-speech and play the sound here
            # using instructions[1] as the text to be said.
        else:
            print("Invalid command: %s" % (instructions[0]))

        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue='audio_output', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
