import speech_recognition as sr
import time
import pyaudio
import config.py
import topics.py

# config.wakeWords
# config.wakeWordDetector
# config.intents

def findIntent(text):
    # Check if inform:
    for tw in config.informTriggerWords:
        if tw in text:
            for topic in topics.topics:
                for topicTws in topic["triggerWords"]:
                    for topicTw in topicTws:
                        if topicTw in text:
                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]
            # If no triggerwords were triggered but we still want a response:
            return {"intent": "inform", "responseWanted": True, "topic": "unknown"}
    # Check if joke:  
    for tw in config.jokeTriggerWords:
        if tw in text:
            return {"intent": "joke", "responseWanted": True}
    for tw in config.laughTriggerWords:
        if tw in text:
            return {"intent": "laugh", "responseWanted": False}
    for tw in config.nodTriggerWords:
        if tw in text:
            return {"intent": "nod", "responseWanted": False}
    for tw in config.shakeTriggerWords:
        if tw in text:
            return {"intent": "shake", "responseWanted": False}
    for tw in config.sleepTriggerWords:
        if tw in text:
            return {"intent": "sleep", "responseWanted": False}
    return {"intent": "unknown", "responseWanted": False}
    
def cleanText(query):
    textList = query.split()
    for i in range(len(textList)):
        if textList[i] in config.misspelledOrdina:
            textList[i] = "ordina"
        elif textList[i] in config.misspelledRobot:
            textList[i] = "robot"
    fixedText = " ".join(str(word) for word in textList)
    return fixedText
    
def recognizeSpeech(audio):
    if config.speechRecognizer == "whisper":
        return r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=prompt).lower()
    elif config.speechRecognizer == "witSR":
        return r.recognize_wit(audio, key=witKey).lower()
    elif config.speechRecognizer == "whisperOnline":
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)
        return transcription.text
    elif config.speechRecognizer == "witAI":
        response = client.speech(f, {'Content-Type': 'audio/wav'})
        return response
    
def speak(text):
    if config.speechSynthesizer == "piper":
        command = "echo " + text + " | piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
        result = run(command, hide=True, warn=True)
        if result.ok:
            audio = AudioSegment.from_file("soundbyte.wav", format="wav")
            # return audio
            play(audio)

def respond(intent, topic):
    if intent == "inform":
        if config.responseGenerator == "custom":
            return topics.information[topic]
    elif intent == "joke":
        if config.responseGenerator == "custom":
            return "Wat is rood en slecht voor je tanden, een baksteen"
    
if config.speechRecognizer == "witSR" or config.speechRecognizer == "witAI":
    witKeyFile = open("witkey.txt", "r")
    witKey = witKeyFile.readline().rstrip()
    witKeyFile.close() 

if config.speechRecognizer == "witAI":
    from wit import Wit
    client = Wit(witKey)

if config.speechRecognizer == "whisperOnline":
    from openai import OpenAI 
    client = OpenAI()
else: 
    r = sr.Recognizer()

with sr.Microphone() as source:
    while True:
        awake = False
        audio = r.listen(source)
        start = time.time()
        # Record speech and save it
        with open("microphone-results.wav", "wb") as recording:
            recording.write(audio.get_wav_data())
        # Process speech
        with open("microphone-results.wav", "rb") as audio:
            recognition = recognizeSpeech(audio)
        # Clean text
        query = cleanText(recognition)
        # Decide intent
        foundIntent = findIntent(query)
        intent = foundIntent["intent"]
        shouldReply = foundIntent["responseWanted"]
        topic = foundIntent["topic"]
        if intent["responseWanted] == True:
            # Come up with response:
            response = respond(intent, topic)
            # Speak:
            speak(response)
        else:
            if intent == "sleep":
                # sleep
                print("Going to sleep")
            elif intent == "nod":
                # nod
                print("nodding")
            elif intent == "shake":
                # shake
                print("shaking")
            elif intent == "laugh":
                # laugh
                print("laughing")
            else:
                speak("Ik weet niet precies wat je van me wil, of ik heb je niet goed verstaan, probeer het nog een keertje.")