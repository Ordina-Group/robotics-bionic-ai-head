# How to config:
# There's a few variables that list different options, like speechrecognizers and voskModels. These list a few possible options.
# If you wish to change the selected option, simply change the variable that refers to the list, to refer to another index of the referred-to-list.
# For example, if you wish to select change the speech recognition solution to vosk, change 
# 'speechRecognizer = recognizers[0]' to 'speechRecognizer = recognizers[3]'
# Besides that, there's a few common misspellings of certain words. If you run into a new one, add it to the list.
# Same goes for intents and trigger words. If you wish to change the topics the robot can talk about, see topics.py
# If you write a new intent, make sure to also add it here.

# Misspellings of Ordina. Becomes obsolete once the company's name changes to Sopra Steria
misspelledOrdina = ["ordinna", "ordeena", "oortina", "ortina", "oordinnen", "mordina", "fordina", "jordina", "ordine", "marina", "olina", "ordinnen", "oordingen"]

# Misspellings of robot
misspelledRobot = ["gopelt", "robelt", "hopelt", "globalte", "vanopot", "reelbot", "koppelt", "robert", "ook op", "geopend", "kookpot", "geboekt", "kook pot", "gekoppeld", "ogen", "opgenomen", "ego pod", "ego bod"]
misspelledMelvin = ["melvin", "elf in"]

# Words that wake up the robot. Only relevant for "custom" wakeWordDetector
wakeWords = ["robot", "melvin"]

# WakeWord detectors
# As of writing, only "custom" has been implemented.
wakeWordDetectors = ["custom", "snowboy", "porcupine", "raven", "precise"]
wakeWordDetector = wakeWordDetectors[0]

# Speech recognition
recognizers = ["whisper", "witAI", "whisperOnline", "witSR", "vosk"]
speechRecognizer = recognizers[0]
voskModels = ["option1", "option2"]
voskModel = voskModels[0]

# Intents
intents = ["job", "inform", "joke", "laugh", "nod", "shake", "sleep", "funfact"]

# Words that trigger certain intents. Misspellings are included due to the less than 100% accuracy of all speech recognizers
jobTriggerWords = ["baan voor me", "ik zoek werk", "werk voor me", "zoek nog een baan", "zoek een baan", "werk voor mij", "baan voor mij", "zoek nog werk",\
"zoek naar werk", "zoek naar een baan", "vacature open", "factuur open", "baan aanbod", "baan aanbieden", "werk aanbieden", "baan aan bieden", "werk aan bieden"]
funFactTriggerWords = ["grappig feitje", "leuk feitje", "fun fact", "leuk feit", "grappig feit"]
informTriggerWords = ["vertel me", "me vertellen", "informatie", "meer weten", "meer vertellen", "iets vertellen", "wat vertellen", "iets weten", "vertellen over", "hoe zit het met", "wat weet je", "vertel over", "stellen over"]
jokeTriggerWords = ["grapje", "grap", "mopje", "mop", "iets grappigs"]
laughTriggerWords = ["lachen", "lach voor me", "lach eens", "lag voor me", "lag eens"]
nodTriggerWords = ["knik ja", "ja knikken"]
shakeTriggerWords = ["nee schudden", "schud nee", "schudt nee", "schut nee"]
sleepTriggerWords = ["slaap", "slapen"]

# Response GeneratorExit
# As of writing, only "custom" has been implemented, due to the hardware restrictions of the Raspberry Pi 4b.
# Would like to add support for chatgpt, claude, gpt-nl - but have not yet due to lack of license
responseGenerators = ["custom", "llama", "geitje", "fietje"]
responseGenerator = responseGenerators[0]

# Prompt for online models, for increased accuracy
commonWords = ["ordina", "robot", "sopra", "steria", "melvin"]
explanation = "Het volgende is een Nederlandse spraakinput richting een robot bij Ordina, een bedrijf actief binnen de IT. De volgende woorden komen waarschijnlijk voor: "
commonWordsString = ", ".join(str(word) for word in commonWords)
prompt = explanation + commonWordsString