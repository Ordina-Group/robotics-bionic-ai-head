# Explanation of this file: 
# This is a configuration file for the topics the robot can talk about.
# The list topics is a collection of different topics. Each topic has a dictionary of words related to it that trigger said topic.
# For example, if you want to be informed about the offices, there are more than 1 way of asking for information about them.
# It would be unwise to associate only 1 word with each topic. Therefore, a dictionary of values or synonyms is associated with each topic.
# If you find the robot does not trigger when you want it to, add a synonym to the relevant dictionary.
# After the topics list follows the information you wish to share with the crowd. Change according to need.

# IMPORTANT!!!
# If you add a new topic, make sure to add the of the dictionary to the 'InformationClass' class,
# and make a corresponding method. These get called dynamically when information gets requested.
# ALSO IMPORTANT!!
# If you decide to use Piper tts, some of the voices act weird if a sentence has too little words.
# Therefore, instead of ending the sentence (.), use a comma (,) to prolong it.

office = {"triggerWords": ["kantoor", "kantoren", "locaties"], "topic": "kantoor"}
staff = {"triggerWords": ["personeel", "collega's", "collega", "medewerker", "medewerkers"], "topic": "personeel"}
pay = {"triggerWords": ["salaris", "loon", "uurtarief"], "topic": "salaris"}
clients = {"triggerWords": ["klanten", "werkgever", "werkgevers", "opdrachtgever", "opdrachtgevers"], "topic": "klanten"}
internships = {"triggerWords": ["stageopdracht", "stageopdrachten", "stage opdracht", "stage opdrachten", "stagemogelijkheden", "stage mogelijkheden", "stagemogelijkheid", "stage mogelijkheid"], "topic": "stage"}
assignments = {"triggerWords": ["opdracht", "opdrachten"], "topic": "opdrachten"}
company = {"triggerWords": ["bedrijf Ordina", "jullie bedrijf", "je bedrijf", "organisatie", "sopra steria", "wie zijn jullie", "wie jullie zijn"], "topic": "bedrijf"}
workEnvironment = {"triggerWords": ["werksfeer", "sfeer op kantoor"], "topic": "werksfeer"}
whatWeDo = {"triggerWords": ["wat jullie doen", "wat jullie zo al doen"], "topic": "watDoen"}
robot = {"triggerWords": ["robot", "robothoofd", "robot hoofd", "melvin", "dit hoofd"], "topic": "robot"}
strategy = {"triggerWords": ["strategie"], "topic": "strategie"}
whyWereHereToday = {"triggerWords": ["waarom jullie hier vandaag zijn", "wat jullie hier vandaag doen", "wat jullie hier doen", "waarom jullie hier zijn"], "topic": "hierVandaag"}

topics = [office, staff, pay, clients, assignments, company, internships, workEnvironment, whatWeDo, robot, strategy, whyWereHereToday]

information = {"kantoor": "Ordina heeft negen kantoren in Nederland, België en Luxemburg, het hoofdkantoor bevindt zich in Nieuwegein.",\
 "personeel": "Ordina heeft ongeveer drie duizend medewerkers, waarvan zeker tachtig procent in Nederland. De gemiddelde leeftijd ligt rond de dertig, en ongeveer twintig procent van de medewerkers is vrouwelijk of non-binair, we zoeken altijd nieuwe collegas",\
 "salaris": "Ordina is heel transparant in hun salarisverdeling, mijn salaris als robot hoofd is nul ha ha ha ha",\
 "klanten": "We hebben klanten door heel de Beeneluux heen, bijvoorbeeld Defensie of de Rabobank.",\
 "stage": "Sowieso dat we een leuke staazje opdracht hebben liggen, ik ben daar één van, ik ben gemaakt door een staazjeer, verdeeld over twee staazje periodes. Vraag vooral om meer informatie bij een van mijn begeleiders.",\
"opdrachten": "We hebben opdrachten voor een grote hoeveelheid verschillende klanten. De ene is spannender dan de andere, ik heb zelf geen werkervaring, maar de mensen om me heen wel!",\
"bedrijf": "Ordina is in negentien drie en zeventig opgericht, en in twee duizend drie en twintig overgekocht door Soopra Steria, we zijn gespecialiseerd in I T consultancy.",\
"werksfeer": "Ondanks dat we een relatief groot bedrijf zijn, heerst er een fijne en gezellige werksfeer. We gaan regelmatig op uitjes naar evenementen als deze, of bijvoorbeeld de Efteling",\
"watDoen": "tekst!",\
"robot": "Ik ben een robot, in elkaar gezet en herontworpen door Marten Elsinga, een staazjeer bij Ordina. Ik draai op een raspberry paai vier b, mijn naam is Melvin, aangenaam kennis te maken",\
"strategie": "tekst!",\
"hierVandaag": "We zijn hier vandaag op tek nee sjon om onszelf te preesenteeren aan jou, misschien een toekomstige collega of zakenpartner"}