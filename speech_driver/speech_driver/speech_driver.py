import speech_recognition as sr
import time
import pyaudio
import speech_driver.speech_driver.config as speech_config
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

client = None
awake = False
is_paused = False
r = None

async def main():
    """
    Class to control the microphone connected to the hardware.
    Listens to what the user says, then acts accordingly.
    All configured through speech_config.py
    
    ...
    
    Methods:
    --------
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
        audio_input_queue = await channel.declare_queue("audio_input", auto_delete=False)
        global client
        global awake
        awake = False
        global is_paused
        is_paused = False
        
        async def initialise():
            global client
            """This method initialises witAI or whisperOnline if necessary."""
            if speech_config.speechRecognizer == "witAI":
                witKeyFile = open("witkey.txt", "r")
                witKey = witKeyFile.readline().rstrip()
                witKeyFile.close()   
                from wit import Wit
                client = Wit(witKey)
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
        
        def first_value(obj, key):
            if key not in obj:
                return None
            val = obj[key][0]["value"]
            if not val:
                return None
            return val
        
        async def recognizeSpeech(audio):
            """This method recognizes user input with speech depending on speech_config.speechRecognizer, which defaults to whisper."""
            
            if speech_config.speechRecognizer == "whisper":
                model = "small"
                language = "dutch"
                initial_prompt = speech_config.prompt
                returnedSpeech = await asyncio.to_thread(recogn_whisper, audio, model, language, initial_prompt)                
                query = cleanText(returnedSpeech)
                print(query)
                reply = "respond:::" + query
                await publish(reply, "hub")
            elif speech_config.speechRecognizer == "witSR":
                return r.recognize_wit(audio, key=witKey).lower()
            elif speech_config.speechRecognizer == "whisperOnline":
                transcription = r.audio.transcriptions.create(model="whisper-1", file=audio)
                return transcription.text
            elif speech_config.speechRecognizer == "witAI":
                """
                with open("microphone-results.wav", "rb") as recording: 
                ### TODO!!
                intent = None
                topic = None
                responseWanted = True
                response = client.speech(recording, {"Content-Type": "audio/wav"})
                print(response)
                entities = response["entities"]
                ### DIT WERKT NOG NIET!!
                if entities[0]["name"] == "informationEntity:informationEntity":
                    intent = "inform"
                possible_topic = first_value(entities, "informationEntity:informationEntity")
                topic = None
                if possible_topic:
                    topic = possible_topic
                print(entity)
                topic = None
                #if possible_topic:
                    #topic = possible_topic
                return {"intent": intent, "responseWanted": True, "topic": None}
                
                if responseWanted:
                    query = "{intent}***{responseWanted}***{topic}***{text}"
                    print("Intent: " + {intent} + ", should respond: " + {responseWanted} + ", topic: " + {topic} + ", text: " + {text})
                    return query
                else:
                    query = "{intent}***False***{topic}***{text}"
                    print("Intent: " + {intent} + ", should respond: False, topic: " + {topic} + ", text: " + {text})
                    // Doe iets adhv intent
                    return query    
                """
                return {"intent": None, "responseWanted": False, "topic": None}
            elif speech_config.speechRecognizer == "vosk":
                raise Exception("Not implemented yet")
        
        def listen(source, max_duration, min_duration):
            audio = r.listen(source, max_duration, min_duration)
            with open("microphone-results.wav", "wb") as recording:
                recording.write(audio.get_wav_data())
            return audio

        def wakeUp_sync(stream, recognizer):
            global awake
            global is_paused
            while True:
                if awake == False and is_paused == False:
                    data = stream.read(4096, exception_on_overflow = False)
                    if recognizer.AcceptWaveform(data):
                        text = recognizer.Result()
                        cleanQuery = cleanWakeUp(text[14:-3])
                        print(cleanQuery)
                        for wakeUpWord in speech_config.wakeWords:
                            if wakeUpWord in cleanQuery:
                                awake = True
                                return
                if awake == True:
                    return

        async def wakeUp(recognizer):
            """This method starts a while True loop that is constantly checking to see if the robot should wake up or not.
            It uses VOSK to detect speech input and is only used if speech_config.wakeWordDetector == custom."""
            
            mic = pyaudio.PyAudio()
            stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
            stream.start_stream()
            await asyncio.to_thread(wakeUp_sync, stream, recognizer)
            return
         
        #TODO: DEZE HERSCHRIJVEN OM OP PAUZE TE GAAN
        async def act():
            """This method makes the head act. It is the loop that will be used the most."""
            with sr.Microphone() as source:
                while True:
                    audio = await asyncio.to_thread(listen, source, 12, 5)
                    with open("microphone-results.wav", "wb") as recording:
                        recording.write(audio.get_wav_data())
                    duration = librosa.get_duration(path="microphone-results.wav")
                    if duration > 1:
                        print("Done recording")
                        await publish("move:::sus", "hub")
                        recognition = await recognizeSpeech(audio)
                        reply = ""
                        if speech_config.speechRecognizer == "witAI":
                            reply = "respondWit:::" + recognition
                        else:
                            reply = "respond:::" + recognition
                        await publish(reply, "hub")   
        
        #TODO: DEZE HERSCHRIJVEN OM REKENING TE HOUDEN DAT RESPONSEDRIVER NU HET DENKEN DOET
        async def actLoop(timeOutLimit = 4):
            """This method starts a loop where the robothead does things."""
            global awake
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
                            awake = False
                            return
                    else:
                        awake = False
                        return
                awake = False
                return
        
        async def callback(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process(ignore_processed=True):
                global awake
                await message.ack()
                print("Speech: Message received: " + message.body.decode())
                instructions = message.body.decode().split(":::")
                if instructions[0] == "pause":
                    global is_paused
                    is_paused = True
                    print("paused")
                    pause_timer = int(instructions[1]) / 10
                    await asyncio.sleep(pause_timer)
                    print("unpaused")
                    is_paused = False
                elif instructions[0] == "wakeup":
                    awake = True
                elif instructions[0] == "sleep":
                    awake = False
        
        async def consume_queue():
            await audio_input_queue.consume(callback)
            try:
                await asyncio.Future()
            finally:
                await connection.close()
        
        client = await initialise()
        global r
        r = sr.Recognizer()             
        
        async def main_event_loop(recognizer):
            while True:
                await wakeUp(recognizer)
                await actLoop()
        
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
                await asyncio.gather(main_event_loop(recognizer), consume_queue())
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