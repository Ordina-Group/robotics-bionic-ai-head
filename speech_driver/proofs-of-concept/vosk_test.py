from vosk import Model, KaldiRecognizer
import pyaudio

#model = Model(r"C:\Users\mel33434\Desktop\vosk\vosk-model-nl-spraakherkenning-0.6-lgraph")
model = Model(r"C:\Users\mel33434\Desktop\vosk\vosk-model-small-nl-0.22")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
print("Geluid aan het opnemen")

while True:
    data = stream.read(4096, exception_on_overflow = False)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text[14:-3])