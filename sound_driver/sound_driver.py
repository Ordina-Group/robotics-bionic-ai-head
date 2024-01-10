import os
import pika
import sys
import sounddevice as sd
import soundfile as sf
import numpy

def main():
    kit = ServoKit(channels=16)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='servo_output')
    
    # TODO - specify audio file path
    audio_file_path = 'audio_file.wav'
    
    def callback(ch, method, properties, body):
        command = body.decode.split(':')
        if command[0] == 'play_sound':
            audio_data, fs = sf.read(audio_file_path, dtype='float32')
            sd.play(audio_data, fs)
            sd.wait()
        elif command[0] == 'speak':
            # Add functionality to generate text-to-speech and play the sound here
            # using command[1] as the text to be said.
        else:
            print("Invalid command: %s" % (command[0]))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue='servo', on_message_callback=callback)

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
