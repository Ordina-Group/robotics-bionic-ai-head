import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from pydub.playback import play


class KeywordActivationClass:
    def test(self):
        print("Test method called")
    
    def licht(self):
        print("Licht method called")
        
    def knipper(self):
        print("Knipper method called")
        
    def spraak(self, arg):
        spraak = arg.split("robot")
        echo_command = ["echo", arg]
        piper_speaker =  0 #[0,7,8,17,20,40,41,42,44,45,49,50,51]  
        piper_command = ["piper", "-m", "nl_NL-mls-medium.onnx", "-s", str(piper_speaker), "-f", "soundbyte.wav"]
        echo_process = subprocess.Popen(echo_command, stdout=subprocess.PIPE, shell=True) #Usage of 'shell=True' is dangerous! Use with caution, not necessary on rpi
        piper_process = subprocess.Popen(piper_command, stdin=echo_process.stdout)
        echo_process.wait()
        piper_process.wait()
        audio = AudioSegment.from_file("soundbyte.wav", format="wav")
        play(audio)

    def vraag(self, arg):
        question = arg.split("vraag")
        print(question[1])
        
r = sr.Recognizer()
activationFunction = KeywordActivationClass()
commonWords = ["ordina", "robot"]
prompt = ", ".join(str(word) for word in commonWords)
# According to the Whisper documentation, the model only considers the first 244 tokens of the prompt. Therefore, the common words should remain a short list.
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    awake = False
    while True:
        audio = r.listen(source)
        print("Audio opgenomen.")
        
        keywords = ["licht", "test", "knipper", "spraak", "vraag"]
        spokenText = r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=prompt).lower()
        print("Audio herkend: " + spokenText)
        print("Aan het verwerken...")
        mistakeList = ["ordinna", "ordeena", "gopelt", "robelt", "oortina", "hopelt", "globalte", "vanopot", "ortina", "reelbot", "oordinnen"]
        correctedList = ["ordina", "ordina", "robot", "robot", "ordina", "robot", "robot", "robot", "ordina", "robot", "ordina"]
        # With the introduction of 'initial_prompt' in the r.recognize_whisper, mistake correction becomes almost unnecessary. 
        # However, it is still applied here to improve performance.
        for i in range(len(mistakeList)):
            textList = spokenText.split()
            for y in range(len(textList)):
                if textList[y] == mistakeList[i]:
                    textList[y] = correctedList[i]
            fixedText = " ".join(str(word) for word in textList)
        if "robot" in fixedText or awake == True:
            awake = True
            answered = False
            for keyword in keywords:
                if keyword in fixedText and answered == False:
                    answered = True
                    if keyword == "spraak" or keyword == "vraag":
                        print(fixedText)
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method(fixedText)
                    else:
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method()
        print(fixedText)
        