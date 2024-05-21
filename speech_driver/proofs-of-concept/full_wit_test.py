from wit import Wit
import speech_recognition as sr
import time

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
        response = None
        with open("audio.wav", "rb") as f:
            response = client.speech(f, {'Content-Type': 'audio/wav'})
        end = time.time()
        print(f"Spraak herkend in {end - start} seconden")
        print(response)
        #entities = response["entities"]
        #toBeFixedEntity = first_value(entities, "informationEntity:informationEntity")
        #informationEntity = None
        #if toBeFixedEntity:
            #informationEntity = fix_query(toBeFixedEntity)
        #intents = response["intents"]
        #intent = intents[0]
        #if intent["name"] == "inform" and informationEntity:
            #print("Je wil geïnformeerd worden over " + informationEntity)
        # elif intent["name"] == "joke" and 
