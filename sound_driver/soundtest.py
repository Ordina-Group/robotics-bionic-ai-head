import os
import sys
import sounddevice as sd
import soundfile as sf

def main():
    # TODO - specify audio file path
    audio_file_path = 'oof.wav'
    audio_data, fs = sd.read(audio_file_path, dtype='float32')
    sd.play(audio_data, fs)
    sd.wait()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
