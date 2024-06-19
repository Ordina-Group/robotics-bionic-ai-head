import speech_recognition as sr
import time
import pyaudio
import speech_driver.speech_driver.config as speech_config
import speech_driver.speech_driver.topics as speech_topics
from speech_driver.speech_driver.funfacts import funFacts as funFact
from speech_driver.speech_driver.jokes import jokes as jokes
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import os
import sys
import signal
import pika
import random
import librosa
import asyncio
import aio_pika
from invoke import run

async def main():
    """
    Class to control the microphone connected to the hardware.
    Listens to what the user says, then acts accordingly.
    All configured through speech_config.py
    
    ...
    
    Methods:
    --------
    findIntent(text: string)
        Finds the user's intentions through filtering for certain triggerwords. Used only if speech_config.speechRecognizer != witAI.
    cleanWakeUp(query: string)
        Cleans up a WakeUp Query by looking for words the application commonly mistakes when saying the WakeWord. Only used if speech_config.wakeWordDetector == custom.
        Added because VOSK does not easily support a custom dictionary.
    cleanText(query: string)
        Cleans up a query by comparing words to a list of words the application gets wrong often when saying words like 'Ordina' or 'Sopra Steria'.
    recognizeSpeech(audio: audiofile)
        Recognises user input speech, using a solution depending on speech_config.py.
    initialise()
        Creates an instance of WitAI or online WhisperAPI if necessary. Due to not having a license for WhisperAPI, only WitAI works and only on Marten Elsinga's Wit App. Contact me if necessary.
    act()
        After waking up, tries to record speech to then be sent to recognizeSpeech(), then decides if it should respond or not.
    wakeUp(recognizer: speech_recognition.recognizer_instance)
        Continuous while True loop to see if the robot has to wake up. Uses VOSK by default.
    actLoop(timeOutLimit: int)
        Starts a continuous while True loop that checks if act() has successfully been called. If not successful after timeOutLimit (default = 4) or if successfully called act(), returns out of the loop.
    """    
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        global client
        
        async def initialise():
            """This method initialises witAI or whisperOnline if necessary."""
            if speech_config.speechRecognizer == "witAI":
                from wit import Wit
                return Wit(witKey)
            elif speech_config.speechRecognizer == "whisperOnline":
                from openai import OpenAI 
                return OpenAI()
            else: 
                return
        
        async def publish(message, routing_key):
            print("Speech: message sent! " + message)
            await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
            return


        async def findIntent(text):
            """
            This method finds the intent of the user depending on what they said. This method only gets called if speech_config.speechRecognizer != witAI.
            """
            if speech_config.responseGenerator != "custom":
                return {"intent": "response", "responseWanted": True, "topic": None}
            if speech_config.speechRecognizer != "witAI":
                for tw in speech_config.jobTriggerWords:
                    if tw in text:
                        return {"intent": "job", "responseWanted": True, "topic": None}
                for tw in speech_config.funFactTriggerWords:
                    if tw in text:
                        return {"intent": "funfact", "responseWanted": True, "topic": None}
                afterOver = text.split("over")
                for tw in speech_config.informTriggerWords:
                    if tw in text:
                        for topic in speech_topics.topics:
                            for topicTw in topic["triggerWords"]:
                                if len(afterOver) > 1:
                                    if topicTw in afterOver[1]:
                                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                                    elif topicTw in text:
                                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                        return {"intent": "inform", "responseWanted": True, "topic": "unknown"}
                for tw in speech_config.jokeTriggerWords:
                    if tw in text:
                        return {"intent": "joke", "responseWanted": True, "topic": None}
                for tw in speech_config.laughTriggerWords:
                    if tw in text:
                        return {"intent": "laugh", "responseWanted": False, "topic": None}
                for tw in speech_config.nodTriggerWords:
                    if tw in text:
                        return {"intent": "nod", "responseWanted": False, "topic": None}
                for tw in speech_config.shakeTriggerWords:
                    if tw in text:
                        return {"intent": "shake", "responseWanted": False, "topic": None}
                for tw in speech_config.sleepTriggerWords:
                    if tw in text:
                        return {"intent": "sleep", "responseWanted": False, "topic": None}
                return {"intent": "unknown", "responseWanted": False, "topic": None}
            if speech_config.speechRecognizer == "witAI":
                raise Exception("findIntent() should not get called when using witAI")

        def cleanWakeUp(query):
            """This method cleans up a WakeUp query. It should only be used if speech_config.wakeWordDetector == custom. This method exists because VOSK, which is used for the custom wakeWordDetection, is prone to misunderstanding words."""
            
            if speech_config.wakeWordDetector != "custom":
                raise Exception("cleanWakeUp should not be used when using any other WakeWordDetector than the custom one")
            else:
                textList = query.split()
                for i in range(len(textList)):
                    if textList[i] in speech_config.misspelledRobot:
                        textList[i] = "robot"
                    elif len(textList) > i + 1:
                        if textList[i] + " " + textList[i + 1] in speech_config.misspelledRobot:
                            textList[i] = "robot"
                            textList[i + 1] = ""
                fixedText = " ".join(str(word) for word in textList)
                return fixedText

        def cleanText(query):
            """This method gets called to clean up the recognized text. It exists because certain words like Ordina or Sopra Steria don't exist in many dictionaries."""
            
            textList = query.split()
            for i in range(len(textList)):
                if textList[i] in speech_config.misspelledOrdina:
                    textList[i] = "ordina"
                elif textList[i] in speech_config.misspelledRobot:
                    textList[i] = "robot"
            fixedText = " ".join(str(word) for word in textList)
            return fixedText
        
        def recogn_whisper(audio, model, language, initial_prompt):
            return r.recognize_whisper(audio, model=model, language=language, initial_prompt=initial_prompt).lower()
        
        async def recognizeSpeech(audio):
            """This method recognizes user input with speech depending on speech_config.speechRecognizer, which defaults to whisper."""
            
            if speech_config.speechRecognizer == "whisper":
                model = "small"
                language = "dutch"
                initial_prompt = speech_config.prompt
                returnedSpeech = await asyncio.to_thread(recogn_whisper, audio, model, language, initial_prompt)
                return returnedSpeech
                #return r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=speech_config.prompt).lower()
            elif speech_config.speechRecognizer == "witSR":
                return r.recognize_wit(audio, key=witKey).lower()
            elif speech_config.speechRecognizer == "whisperOnline":
                transcription = r.audio.transcriptions.create(model="whisper-1", file=audio)
                return transcription.text
            elif speech_config.speechRecognizer == "witAI":
                response = client.speech(f, {"Content-Type": "audio/wav"})
                return response
            elif speech_config.speechRecognizer == "vosk":
                raise Exception("Not implemented yet")
        
        def run_command_sync(command):
            run(command, hide=True, warn=True)
        
        async def respond(intent, topic, text):
            """This method generates a response, depending on speech_config.responseGenerator, which defaults to custom. Most of the alternatives have not been implemented yet."""
            if speech_config.responseGenerator == "custom":
                if intent == "job":
                    return "We zijn altijd op zoek naar collegaas, en hoewel ik je zelf niet iets aan kan bieden verwijs ik je graag door naar de mensen die me vandaag hebben meegenomen"
                if intent == "inform":
                    if topic == "unknown":
                        subject = list(text.split(" "))
                        print(subject[-1])
                        return "Ik hoor dat je over " + subject[-1] + " geïnformeerd wil worden, maar ik heb daar geen kennis over."
                    else:
                        return speech_topics.information[topic]
                elif intent == "joke":
                    random.seed(time.time())
                    return random.choice(jokes)
                elif intent == "funfact":
                    random.seed(time.time())
                    fact = random.choice(funFacts)
                    return "Wist je dat " + fact
            else:
                if speech_config.responseGenerator == "fietje":
                    command = "echo " + text + " in zinnen van minimaal 10 en maximaal 20 woorden " + " | ollama run bramvanroy/fietje-2b-chat:Q3_K_M > output.txt"
                elif speech_config.responseGenerator == "llama":
                    command = "echo " + text + " | ollama run llama3 > output.txt"
                elif speech_config.responseGenerator == "geitje":
                    command = "echo " + text + " | ollama run bramvanroy/geitje-7b-ultra-gguf > output.txt"
                await asyncio.to_thread(run_command_sync, command)
                file = file = open("output.txt", "r")
                text = file.read()
                file.close()
                return text
                          
        
        def listen(source, max_duration, min_duration):
            audio = r.listen(source, max_duration, min_duration)
            with open("microphone-results.wav", "wb") as recording:
                        recording.write(audio.get_wav_data())
            return audio
            
        async def act():
            """This method makes the head act. It is the loop that will be used the most."""
            with sr.Microphone() as source:
                while True:
                    audio = await asyncio.to_thread(listen, source, 12, 5)
                    #r.listen(source, 12, 5)
                    with open("microphone-results.wav", "wb") as recording:
                        recording.write(audio.get_wav_data())
                    duration = librosa.get_duration(path="microphone-results.wav")
                    if duration > 1:
                        print("Done recording")
                        await publish("move:::sus", "hub")
                        recognition = await recognizeSpeech(audio)
                        query = cleanText(recognition)
                        print(query)
                        foundIntent = await findIntent(query)
                        intent = foundIntent["intent"]
                        shouldReply = foundIntent["responseWanted"]
                        topic = foundIntent["topic"]
                        if shouldReply == True:
                            response = await respond(intent, topic, query)
                            reply = "speak:::" + response
                            await publish(reply, "hub")
                            if topic != "unknown":
                                return True
                            else:
                                return False
                        else:
                            if intent == "sleep" or intent == "nod" or intent == "shake" or intent == "laugh":
                                reply = "move:::" + intent
                                await publish(reply, "hub")
                                return True
                            else:
                                await publish("move:::rest", "hub")
                                print("Ik heb je niet goed verstaan. Probeer het nog eens.")
                    

        def wakeUp_sync(stream, recognizer):
            while True:
                data = stream.read(4096, exception_on_overflow = False)
                if recognizer.AcceptWaveform(data):
                    text = recognizer.Result()
                    cleanQuery = cleanWakeUp(text[14:-3])
                    print(cleanQuery)
                    for wakeUpWord in speech_config.wakeWords:
                        if wakeUpWord in cleanQuery:
                            return

        async def wakeUp(recognizer):
            """This method starts a while True loop that is constantly checking to see if the robot should wake up or not.
            It uses VOSK to detect speech input and is only used if speech_config.wakeWordDetector == custom."""
            
            mic = pyaudio.PyAudio()
            stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
            stream.start_stream()
            await asyncio.to_thread(wakeUp_sync, stream, recognizer)
            return
            
        async def actLoop(timeOutLimit = 4):
            """This method starts a loop where the robothead does things."""
            while True:
                acted = False
                timeOut = 0
                while acted == False and timeOut < timeOutLimit:
                    await publish("move:::rest", "hub")
                    acted = await act()
                    if acted == False:
                        timeOut += 1
                        if timeOut == timeOutLimit:
                            print("Ik ben per ongeluk wakker geworden geloof ik. Ik ga weer slapen.")
                            await publish("move:::sleep", "hub")
                            return
                    else:
                        return
                return
        
        
        client = await initialise()
        global r
        r = sr.Recognizer()
        if speech_config.speechRecognizer == "witSR" or speech_config.speechRecognizer == "witAI":
            witKeyFile = open("witkey.txt", "r")
            global witKey
            witKey = witKeyFile.readline().rstrip()
            witKeyFile.close()       
        
        if speech_config.wakeWordDetector == "custom":
            model = Model("speech_driver/vosk/vosk-model-small-nl-0.22")
            recognizer = KaldiRecognizer(model, 16000)
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration = 1)
                r.pause_threshold = 2 # default is 0.8
                os.system("cls" if os.name == "nt" else "clear")
                print("Ready to go")
                awake = False
                await publish("move:::sleep", "hub")
                while True:
                    await wakeUp(recognizer)
                    await actLoop()
        elif speech_config.wakeWordDetector == "snowboy":
            while True:
                print("")
                # Run snowboy until wake word is detected, then act()
        elif speech_config.wakeWordDetector == "porcupine":
            while True:
                print("") # act
        elif speech_config.wakeWordDetector == "raven":
            while True:
                print("")
               # act
        elif speech_config.wakeWordDetector == "precise":
            while True:
                print("")
                # act

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)