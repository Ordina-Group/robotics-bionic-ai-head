from pydub import AudioSegment
from pydub.playback import play

def play_audio():
    #audio = AudioSegment.from_file(path, format=file_type)
    print("play_audio")
    audio = AudioSegment.from_file("sound_driver\\sound_driver\\soundbyte.wav", format="wav")
    play(audio)
    return
    
play_audio()