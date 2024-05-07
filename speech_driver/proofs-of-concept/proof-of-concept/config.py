# How to config:
# There's a few variables that list different options, like synthesizers, recognizers and voskModels. These list a few possible options.
# If you wish to change the selected option, simply change the variable that refers to the list, to refer to another index of the referred-to-list.
# For example, if you wish to select change the speech recognition solution to vosk, change 
# 'speechRecognizer = recognizers[0]' to 'speechRecognizer = recognizers[3]'
# Besides that, there's a few common misspellings of certain words. If you run into a new one, add it to the list.
# Same goes for intents and trigger words. If you wish to change the topics the robot can talk about, see topics.py
# If you write a new intent, make sure to also add it here.

# Misspellings of Ordina. Becomes obsolete once the company's name changes to Sopra Steria
misspelledOrdina = ["ordinna", "ordeena", "oortina", "ortina", "oordinnen", "mordina", "fordina", "jordina", "ordine", "marina", "olina", "ordinnen", "oordingen"]

# Misspellings of robot
misspelledRobot = ["gopelt", "robelt", "hopelt", "globalte", "vanopot", "reelbot"]

# Words that wake up the robot. Only relevant for "custom" wakeWordDetector
wakeWords = ["robot", "melvin"]

# WakeWord detectors
# As of writing, only "custom" has been implemented.
wakeWordDetectors = ["custom", "snowboy", "porcupine", "raven", "precise"]
wakeWordDetector = wakeWordDetectors[0]

# Speech synthesis
synthesizers = ["piper", "option2"]
speechSynthesizer = synthesizers[0]
piperVoices = [0,7,8,17,20,40,41,42,44,45,49,50,51]
piperVoice = piperVoices[0]

# Speech recognition
recognizers = ["whisper", "whisperOnline", "witSR", "vosk", "witAI"]
speechRecognizer = recognizers[0]
voskModels = ["option1", "option2"]
voskModel = voskModels[0]

# Intents
intents = ["inform", "joke", "laugh", "nod", "shake", "sleep"]

# Words that trigger certain intents. Misspellings are included due to the less than 100% accuracy of all speech recognizers
informTriggerWords = ["vertel me", "me vertellen", "informatie", "meer weten", "meer vertellen", "iets vertellen", "wat vertellen", "iets weten", "vertellen over"]
jokeTriggerWords = ["grapje", "grap", "mopje", "mop", "iets grappigs"]
laughTriggerWords = ["lachen", "lach voor me", "lach eens", "lag voor me", "lag eens"]
nodTriggerWords = ["knik ja", "ja knikken"]
shakeTriggerWords = ["nee schudden", "schud nee", "schudt nee", "schut nee"]
sleepTriggerWords = ["slaap", "ga slapen"]

# Response GeneratorExit
# As of writing, only "custom" has been implemented, due to the hardware restrictions of the Raspberry Pi 4b.
responseGenerators = ["custom", "llama", "geitje", "gpt", "claude"]
responseGenerator = responseGenerators[0]

# Prompt for online models, for increased accuracy
commonWords = ["ordina", "robot"]
explanation = "Het volgende is een Nederlandse spraakinput richting een robot bij Ordina, een bedrijf actief binnen de IT. De volgende woorden komen waarschijnlijk voor: "
commonWordsString = ", ".join(str(word) for word in commonWords)
prompt = explanation + commonWordsString