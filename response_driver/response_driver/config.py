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