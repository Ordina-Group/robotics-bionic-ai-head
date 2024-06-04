import speech_recognition as sr

class KeywordActivationClass:
    def test(self):
        print("Test method called")
    
    def licht(self):
        print("Licht method called")
        
    def knipper(self):
        print("Knipper method called")
        
    def spraak(self, arg):
        spraak = arg.split("robot")
        print(spraak[1])

    def vraag(self, arg):
        vraagje = arg.split("vraag")
        print(vraagje[1])
        
r = sr.Recognizer()
activationFunction = KeywordActivationClass()
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    awake = False
    while True:
        audio = r.listen(source)
        print("Nu wordt het verwerkt.")
        keywords = ["licht", "test", "knipper", "spraak", "vraag"]
        spokenText = r.recognize_whisper(audio, language="dutch").lower()
        if "robot" in spokenText or awake == True:
            awake = True
            answered = False
            for keyword in keywords:
                if keyword in spokenText and answered == False:
                    answered = True
                    if keyword == "spraak" or keyword == "vraag":
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method(spokenText)
                    else:
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method()
        print(spokenText)
        