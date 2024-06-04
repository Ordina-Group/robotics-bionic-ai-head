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
        question = arg.split("vraag")
        print(question[1])
        
r = sr.Recognizer()
activationFunction = KeywordActivationClass()
commonWords = ["ordina", "robot"]
explanation = "Het volgende is een Nederlandse spraakinput richting een robot bij Ordina, een bedrijf actief binnen de IT. De volgende woorden komen waarschijnlijk voor: "
commonWordsString = ", ".join(str(word) for word in commonWords)
prompt = explanation + commonWordsString
with sr.Microphone() as source:
    print("Spraakherkenning actief")
    awake = False
    while True:
        audio = r.listen(source)
        print("Nu wordt het verwerkt.")
        keywords = ["licht", "test", "knipper", "spraak", "vraag"]
        spokenText = r.recognize_whisper(audio, model="small", language="dutch", initial_prompt=prompt).lower()
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
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method(fixedText)
                    else:
                        awake = False
                        method = getattr(activationFunction, keyword)
                        method()
        print(fixedText)
        