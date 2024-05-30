import speech_recognition as sr
import time
import pyaudio
import config
import topics
from funfacts import funFacts
from jokes import jokes
from invoke import run
from pydub import AudioSegment
from pydub.playback import play
import librosa
from vosk import Model, KaldiRecognizer
import os
import pika
import random

def findIntent(text):
    """This method finds the intent of the user depending on what they said. This method only gets called if config.speechRecognizer != witAI."""
    
    if config.speechRecognizer != "witAI":
        for tw in config.jobTriggerWords:
            if tw in text:
                return {"intent": "job", "responseWanted": True, "topic": None}
        for tw in config.funFactTriggerWords:
            if tw in text:
                return {"intent": "funfact", "responseWanted": True, "topic": None}
        afterOver = text.split("over")
        for tw in config.informTriggerWords:
            if tw in text:
                for topic in topics.topics:
                    for topicTw in topic["triggerWords"]:
                        if len(afterOver) > 1:
                            if topicTw in afterOver[1]:
                                return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                            elif topicTw in text:
                                return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                return {"intent": "inform", "responseWanted": True, "topic": "unknown"}
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
    if config.speechRecognizer == "witAI":
        raise Exception("findIntent() should not get called when using witAI")

def cleanWakeUp(query):
    """This method cleans up a WakeUp query. It should only be used if config.wakeWordDetector == custom. This method exists because VOSK, which is used for the custom wakeWordDetection, is prone to misunderstanding words."""
    
    if config.wakeWordDetector != "custom":
        raise Exception("cleanWakeUp should not be used when using any other WakeWordDetector than the custom one")
    else:
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
    """This method gets called to clean up the recognized text. It exists because certain words like Ordina or Sopra Steria don't exist in many dictionaries."""
    
    textList = query.split()
    for i in range(len(textList)):
        if textList[i] in config.misspelledOrdina:
            textList[i] = "ordina"
        elif textList[i] in config.misspelledRobot:
            textList[i] = "robot"
    fixedText = " ".join(str(word) for word in textList)
    return fixedText
    
# def recognizeSpeech(audio, r, client):
def recognizeSpeech(audio):
    """This method recognizes user input with speech depending on config.speechRecognizer, which defaults to whisper."""
    
    if config.speechRecognizer == "whisper":
        return r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=config.prompt).lower()
    elif config.speechRecognizer == "witSR":
        return r.recognize_wit(audio, key=witKey).lower()
    elif config.speechRecognizer == "whisperOnline":
        transcription = r.audio.transcriptions.create(model="whisper-1", file=audio)
        return transcription.text
    elif config.speechRecognizer == "witAI":
        response = client.speech(f, {"Content-Type": "audio/wav"})
        return response
    elif config.speechRecognizer == "vosk":
        raise Exception("Not implemented yet")
    
def speak(text):
    """This method generates speech and pronounces it. It should be moved to a seperate driver."""
    
    if config.speechSynthesizer == "piper":
        if os.name == "nt":
            command = "echo " + text + " | piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
        else:
            command = "echo " + text + " | ./piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
        run(command, hide=True, warn=True)
        filePath = "soundbyte.wav"
        audio = AudioSegment.from_file(filePath, format="wav")
        duration = librosa.get_duration(path=filePath)
        durationMs = round(duration * 10)
        command = "speak:" + str(durationMs)
        channel.basic_publish(exchange="", routing_key="servo", body=command)
        channel.basic_publish(exchange="", routing_key="audio_output", body=filePath)
        # return audio
        play(audio)


def respond(intent, topic, text):
    """This method generates a response, depending on config.responseGenerator, which defaults to custom. Most of the alternatives have not been implemented yet."""
    
    if config.responseGenerator == "custom":
        if intent == "job":
            return "We zijn altijd op zoek naar collegaas, en hoewel ik je zelf niet iets aan kan bieden verwijs ik je graag door naar de mensen die me vandaag hebben meegenomen"
        if intent == "inform":
            if topic == "unknown":
                subject = list(text.split(" "))
                print(subject[-1])
                return "Ik hoor dat je over " + subject[-1] + " geïnformeerd wil worden, maar ik heb daar geen kennis over."
            else:
                return topics.information[topic]
        elif intent == "joke":
            random.seed(time.time())
            return random.choice(jokes)
        elif intent == "funfact":
            random.seed(time.time())
            fact = random.choice(funFacts)
            return "Wist je dat " + fact
            
def initialise():
    """This method initialises witAI or whisperOnline if necessary."""
    
    if config.speechRecognizer == "witAI":
        from wit import Wit
        return Wit(witKey)
    elif config.speechRecognizer == "whisperOnline":
        from openai import OpenAI 
        return OpenAI()
    else: 
        return
        

# def act(r, client):
def act():
    """This method makes the head act. It is the loop that will be used the most."""
    
    with r.Microphone() as source:
        while True:
            audio = r.listen(source, 12, 7)
            # Record speech and save it
            with open("microphone-results.wav", "wb") as recording:
                recording.write(audio.get_wav_data())
            # Process speech
            print("Done recording")
            channel.basic_publish(exchange="", routing_key="servo", body="sus")
            # recognition = recognizeSpeech(audio, r, client)
            recognition = recognizeSpeech(audio)
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
                if topic != "unknown":
                    return True
                else:
                    return False
            else:
                if intent == "sleep":
                    # sleep
                    print("Going to sleep")
                    channel.basic_publish(exchange="", routing_key="servo", body=intent)
                    return True
                elif intent == "nod":
                    # nod
                    print("nodding")
                    channel.basic_publish(exchange="", routing_key="servo", body=intent)
                    return True
                elif intent == "shake":
                    # shake
                    print("shaking")
                    channel.basic_publish(exchange="", routing_key="servo", body=intent)
                    return True
                elif intent == "laugh":
                    # laugh
                    print("laughing")
                    channel.basic_publish(exchange="", routing_key="servo", body=intent)
                    return True
                else:
                    print("Ik heb je niet goed verstaan. Probeer het nog eens.")
            

# Implementation for fast speech recognition. Uses VOSK and only used for wake word detection.
def wakeUp(recognizer):
    """This method starts a while True loop that is constantly checking to see if the robot should wake up or not."""
    
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
        else:
            print("Something went wrong - method wakeUp")

def actLoop():
    """This method starts a loop where the robothead does things."""
    
    while True:
        print("Awake")
        acted = False
        timeOut = 0
        timeOutLimit = 4
        while acted == False and timeOut < timeOutLimit:
            channel.basic_publish(exchange="", routing_key="servo", body="rest")
            # acted = act(r, client)
            acted = act()
            if acted == False:
                timeOut += 1
                if timeOut == timeOutLimit:
                    print("Ik ben per ongeluk wakker geworden geloof ik. Ik ga weer slapen.")
                    return
            else:
                print("Oké, ik ga weer slapen.")
                return
        return


# def main(r, client):
def main():
    if config.wakeWordDetector == "custom":
        # relativePath = "speech_driver/vosk/vosk-model-nl-spraakherkenning-0.6-lgraph"
        relativePath = "speech_driver/vosk/vosk-model-small-nl-0.22"
        model = Model(relativePath)
        recognizer = KaldiRecognizer(model, 16000)
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 1)
            # r.pause_threshold = 0.8
            r.pause_threshold = 2
            os.system("cls" if os.name == "nt" else "clear")
            print("Ready to go")
            awake = False
            while True:
                wakeUp(recognizer)
                actLoop()
                channel.basic_publish(exchange="", routing_key="servo", body="sleep")
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
r = sr.Recognizer()
client = initialise()
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="servo")
channel.queue_declare(queue="audio_output")
while True:
    # main(r, client)
    main()
