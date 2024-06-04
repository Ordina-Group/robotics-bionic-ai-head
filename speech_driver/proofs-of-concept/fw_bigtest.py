from faster_whisper import WhisperModel
import speech_recognition as sr
import time

model_size = "small"
model = WhisperModel(model_size, device="cuda", compute_type="float16")
# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

def first_value(obj, key):
    if key not in obj:
        return None
    val = obj[key][0]["value"]
    if not val:
        return None
    return val
    
def fix_query(query):
    mistakeList = ["ordinna", "ordeena", "oortina", "ortina", "oordinnen", "mordina", "fordina", "jordina", "ordine", "marina", "olina"]
    textList = query.split()
    print(textList)
    for i in range(len(textList)):
        if textList[i] in mistakeList:
            textList[i] = "ordina"
    fixedText = " ".join(str(word) for word in textList)
    return fixedText

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    while True:
        audio = r.listen(source)
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("Bestand opgeslagen. Whisper raadplegen.")
        start = time.time()
        segments, info = model.transcribe("microphone-results.wav", beam_size=5, language="nl")
        for segment in segments:
            print(segment.text)
        end = time.time()
        print(f"Spraak herkend in {end - start} seconden")

