import speech_recognition as sr
import time
import pyaudio
import config
import topics
from funfacts import funFacts
from invoke import run
from pydub import AudioSegment
from pydub.playback import play
import librosa
from vosk import Model, KaldiRecognizer
import os
import pika
import random

def findIntent(text):
    # Check if fun fact:
    for tw in config.funFactTriggerWords:
        if tw in text:
            return {"intent": "funfact", "responseWanted": True, "topic": None}
    # Check if inform:
    afterOver = text.split("over")
    for tw in config.informTriggerWords:
        if tw in text:
            for topic in topics.topics:
                for topicTw in topic["triggerWords"]:
                    # This step is added to remove potentials where words earlier in the sentence get detected as the topic.
                    if len(afterOver) > 0:
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

def cleanWakeUp(query):
    textList = query.split()
    for i in range(len(textList)):
        if textList[i] in config.misspelledRobot:
            textList[i] = "robot"
        elif len(textList) > i + 1:
            if textList[i] + " " + textList[i + 1] in config.misspelledRobot:
                textList[i] = "robot"
                textList[i + 1] = ""
    fixedText = " ".join(str(word) for word in textList)
    return fixedText

def cleanText(query):
    textList = query.split()
    for i in range(len(textList)):
        if textList[i] in config.misspelledOrdina:
            textList[i] = "ordina"
        elif textList[i] in config.misspelledRobot:
            textList[i] = "robot"
    fixedText = " ".join(str(word) for word in textList)
    return fixedText
    
def recognizeSpeech(audio, client):
    if config.speechRecognizer == "whisper":
        return client.recognize_whisper(audio, model="small", language="dutch", initial_prompt=config.prompt).lower()
    elif config.speechRecognizer == "witSR":
        return client.recognize_wit(audio, key=witKey).lower()
    elif config.speechRecognizer == "whisperOnline":
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)
        return transcription.text
    elif config.speechRecognizer == "witAI":
        response = client.speech(f, {'Content-Type': 'audio/wav'})
        return response
    
def speak(text):
    if config.speechSynthesizer == "piper":
        if os.name == 'nt':
            command = "echo " + text + " | piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
        else:
            command = "echo " + text + " | ./piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
        run(command, hide=True, warn=True)
        audio = AudioSegment.from_file("soundbyte.wav", format="wav")
        duration = librosa.get_duration(path="soundbyte.wav")
        durationMs = round(duration * 10)
        command = "speak:" + str(durationMs)
        channel.basic_publish(exchange='', routing_key='servo', body=command)
        # return audio
        play(audio)


def respond(intent, topic, text):
    if config.responseGenerator == "custom":
        if intent == "inform":
            if topic == "unknown":
                subject = list(text.split(" "))
                print(subject[-1])
                return "Ik hoor dat je over " + subject[-1] + " geïnformeerd wil worden, maar ik heb daar geen kennis over."
            else:
                return topics.information[topic]
        elif intent == "joke":
            return "Wat is rood en slecht voor je tanden, een baksteen"
        elif intent == "funfact":
            random.seed(time.time())
            return random.choice(funFacts)
            
def initialise():
    if config.speechRecognizer == "witAI":
        from wit import Wit
        return Wit(witKey)
    elif config.speechRecognizer == "whisperOnline":
        from openai import OpenAI 
        return OpenAI()
    else: 
        return sr.Recognizer()

def act(client):
    with sr.Microphone() as source:
        while True:
            audio = client.listen(source)
            # Record speech and save it
            with open("microphone-results.wav", "wb") as recording:
                recording.write(audio.get_wav_data())
            # Process speech
            print("Done recording")
            channel.basic_publish(exchange='', routing_key='servo', body="sus")
            recognition = recognizeSpeech(audio, client)
            # Clean text
            query = cleanText(recognition)
            print(query)
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
                    channel.basic_publish(exchange='', routing_key='servo', body=intent)
                    return True
                elif intent == "nod":
                    # nod
                    print("nodding")
                    channel.basic_publish(exchange='', routing_key='servo', body=intent)
                    return True
                elif intent == "shake":
                    # shake
                    print("shaking")
                    channel.basic_publish(exchange='', routing_key='servo', body=intent)
                    return True
                elif intent == "laugh":
                    # laugh
                    print("laughing")
                    channel.basic_publish(exchange='', routing_key='servo', body=intent)
                    return True
                else:
                    print("Ik heb je niet goed verstaan. Probeer het nog eens.")
            if topic != "unknown" and topic != None:
                return True
            else:
                return False

# Implementation for fast speech recognition. Uses VOSK and only used for wake word detection.
def wakeUp(recognizer):
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    while True:
        data = stream.read(4096, exception_on_overflow = False)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            cleanQuery = cleanWakeUp(text[14:-3])
            print(cleanQuery)
            for wakeUpWord in config.wakeWords:
                if wakeUpWord in cleanQuery:
                    return True

def actLoop():
    while True:
        print("Awake")
        acted = False
        timeOut = 0
        timeOutLimit = 4
        while acted == False and timeOut < timeOutLimit:
            channel.basic_publish(exchange='', routing_key='servo', body="rest")
            acted = act(client)
            if acted == False:
                timeOut += 1
                if timeOut == timeOutLimit:
                    print("Ik ben per ongeluk wakker geworden geloof ik. Ik ga weer slapen.")
            else:
                print("Oké, ik ga weer slapen.")
        return


def main(client):
    if config.wakeWordDetector == "custom":
        # relativePath = "../../vosk/vosk-model-nl-spraakherkenning-0.6-lgraph"
        relativePath = "../../vosk/vosk-model-small-nl-0.22"
        model = Model(relativePath)
        recognizer = KaldiRecognizer(model, 16000)
        with sr.Microphone() as source:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Ready to go")
            awake = False
            while True:
                wakeUp(recognizer)
                actLoop()
                channel.basic_publish(exchange='', routing_key='servo', body="sleep")
    elif config.wakeWordDetector == "snowboy":
        while True:
            print("")
            # Run snowboy until wake word is detected, then act()
    elif config.wakeWordDetector == "porcupine":
        while True:
            print("") # act
    elif config.wakeWordDetector == "raven":
        while True:
            print("")
           # act
    elif config.wakeWordDetector == "precise":
        while True:
            print("")
            # act

if config.speechRecognizer == "witSR" or config.speechRecognizer == "witAI":
    witKeyFile = open("witkey.txt", "r")
    witKey = witKeyFile.readline().rstrip()
    witKeyFile.close() 
client = initialise()
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='servo')
while True:
    main(client)
