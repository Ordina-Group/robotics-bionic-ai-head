from wit import Wit
import speech_recognition as sr
import time

keyFile = open("witkey.txt", "r")
witKey = keyFile.readline().rstrip()
keyFile.close()
client = Wit(witKey)
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    while True:
        audio = r.listen(source)
        start = time.time()
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("Bestand opgeslagen. Wit raadplegen.")
        resp = None
        with open('microphone-results.wav', 'rb') as f:
            resp = client.speech(f, {'Content-Type': 'audio/wav'})
        end = time.time()
        print(f"Spraak herkend in {end - start} seconden")
        print('Wit response: ' + str(resp))
