from invoke import run
from pydub import AudioSegment
from pydub.playback import play

arg = "We zijn hier vandaag op tek nee sjon om onszelf te preesenteeren aan jou, misschien een toekomstige collega of zakenpartner"

piper_speaker =  0 # I found that the following voices work well: [0,7,8,17,20,40,41,42,44,45,49,50,51]  
command = "echo " + arg + " | piper -m nl_NL-mls-medium.onnx -s " + str(piper_speaker) + " -f soundbyte.wav"
result = run(command, hide=True, warn=True)
if result.ok:
    audio = AudioSegment.from_file("soundbyte.wav", format="wav")
    play(audio)