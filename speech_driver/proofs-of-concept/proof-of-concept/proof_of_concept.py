import speech_recognition as sr
import time
import pyaudio
import config
import topics
from invoke import run
from pydub import AudioSegment
from pydub.playback import play
import librosa

# config.wakeWords
# config.wakeWordDetector
# config.intents

def wakeUp(query):
    if config.wakeWordDetector == "custom":
        for wakeUpWord in config.wakeWords:
            if wakeUpWord in query:
                return True
        return False
    elif config.wakeWordDetector == "snowboy":
        print("To be implemented")
    elif config.wakeWordDetector == "hermes":
        print("To be implemented")


def findIntent(text):
    # Check if inform:
    afterOver = text.split("over")
    for tw in config.informTriggerWords:
        if tw in text:
            for topic in topics.topics:
                for topicTw in topic["triggerWords"]:
                    # This step is added to remove potentials where words earlier in the sentence get detected as the topic.
                    if topicTw in afterOver[1]:
                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                    # '!= robot' has to be added to avoid errors regarding the wakeup word.
                    elif topicTw in text and topicTw != "robot":
                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
            # If no triggerwords were triggered but we still want a response:
            return {"intent": "inform", "responseWanted": True, "topic": "unknown"}
    # Check if joke:  
    for tw in config.jokeTriggerWords:
        if tw in text:
            return {"intent": "joke", "responseWanted": True, "topic": None}
    for tw in config.laughTriggerWords:
        if tw in text:
            return {"intent": "laugh", "responseWanted": False, "topic": None}
    for tw in config.nodTriggerWords:
        if tw in text:
            return {"intent": "nod", "responseWanted": False, "topic": None}
    for tw in config.shakeTriggerWords:
        if tw in text:
            return {"intent": "shake", "responseWanted": False, "topic": None}
    for tw in config.sleepTriggerWords:
        if tw in text:
            return {"intent": "sleep", "responseWanted": False, "topic": None}
    return {"intent": "unknown", "responseWanted": False, "topic": None}
    
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
        return r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=config.prompt).lower()
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
            duration = librosa.get_duration(path="soundbyte.wav")
            print(duration)
            # return audio
            play(audio)

def respond(intent, topic, text):
    if intent == "inform":
        if config.responseGenerator == "custom":
            if topic == "unknown":
                subject = list(text.split(" "))
                print(subject[-1])
                return "Ik hoor dat je over " + subject[-1] + " geïnformeerd wil worden, maar ik heb daar geen kennis over."
            else:
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
    print("Ready to go")
    awake = False
    while True:
        audio = r.listen(source)
        start = time.time()
        # Record speech and save it
        with open("microphone-results.wav", "wb") as recording:
            recording.write(audio.get_wav_data())
        # Process speech
        print("Done recording")
        recognition = recognizeSpeech(audio)
        # Clean text
        query = cleanText(recognition)
        print(query)
        # Decide whether to wake up or not
        if awake == False:
            awake = wakeUp(query)
        # Take action if awake
        if awake == True:
            # Decide intent
            foundIntent = findIntent(query)
            intent = foundIntent["intent"]
            shouldReply = foundIntent["responseWanted"]
            topic = foundIntent["topic"]
            if shouldReply == True:
                # Come up with response:
                response = respond(intent, topic, query)
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
                    if "robot" in query:
                        queryList = query.split(" ")
                        # This check is to determine if the user wanted to wakeup the robot or had an actual query
                        if len(queryList) > 3:
                            speak("Ik weet niet precies wat je van me wil, of ik heb je niet goed verstaan, probeer het nog een keertje.")
                    else: 
                        speak("Ik weet niet precies wat je van me wil, of ik heb je niet goed verstaan, probeer het nog een keertje.")
            if topic != "unknown" and topic != None:
                awake = False