import speech_recognition as sr
import time

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    while True:
        audio = r.listen(source)
        before = time.perf_counter()
        print("Nu wordt het verwerkt.")
        spokenText = r.recognize_whisper(audio, language="dutch", model="medium")
        after = time.perf_counter()
        print(spokenText)
        print(f"Daar deed ik {after - before:0.4f} seconden over")
        if spokenText.lower() == "zet het licht aan" or spokenText.lower() == "zet het licht aan.":
            print("Okee, het licht gaat aan.")
        print("Geef nieuwe input.")