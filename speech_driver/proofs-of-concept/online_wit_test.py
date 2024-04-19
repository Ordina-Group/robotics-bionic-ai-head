import speech_recognition as sr
import time

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
        question = arg.split("vraag")
        print(question[1])
        
r = sr.Recognizer()
activationFunction = KeywordActivationClass()
commonWords = ["ordina", "robot"]
explanation = "Het volgende is een Nederlandse spraakinput richting een robot bij Ordina, een bedrijf actief binnen de IT. De volgende woorden komen waarschijnlijk voor: "
commonWordsString = ", ".join(str(word) for word in commonWords)
prompt = explanation + commonWordsString
keyFile = open("witkey.txt", "r")
witKey = keyFile.readline().rstrip()
keyFile.close()
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    awake = False
    while True:
        audio = r.listen(source)
        start = time.time()
        print("Nu wordt het verwerkt.")
        keywords = ["licht", "test", "knipper", "spraak", "vraag"]
        try:
            spokenText = r.recognize_wit(audio, key=witKey).lower()
            end = time.time()
            print(f"Spraak herkend in {end - start} seconden")
            mistakeList = ["ordinna", "ordeena", "gopelt", "robelt", "oortina", "hopelt", "globalte", "vanopot", "ortina", "reelbot", "oordinnen", "mordina", "fordina", "jordina", "ordine", "marina", "olina"]
            correctedList = ["ordina", "ordina", "robot", "robot", "ordina", "robot", "robot", "robot", "ordina", "robot", "ordina", "ordina", "ordina", "ordina", "ordina", "ordina", "ordina"]
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
                            awake = False
                            method = getattr(activationFunction, keyword)
                            method(fixedText)
                        else:
                            awake = False
                            method = getattr(activationFunction, keyword)
                            method()
            print(fixedText)
        except sr.UnknownValueError:
            print("Something went wrong")
        