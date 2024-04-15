import subprocess
import pydub
from pydub.playback import play

#echo_command = ["echo", "Hallo dit is een test!"]
#piper_speaker =  0 #[0,7,8,17,20,40,41,42,44,45,49,50,51]  
#piper_command = ["piper", "-m", "nl_NL-mls-medium.onnx", "-s", str(piper_speaker), "-f", "soundbyte.wav"]
#echo_process = subprocess.Popen(echo_command, stdout=subprocess.PIPE)
#piper_process = subprocess.Popen(piper_command, stdin=echo_process.stdout)
#echo_process.wait()
#piper_process.wait()
#audio = pydub.AudioSegment.from_file("soundbyte.wav", format="wav")
#pydub.playback.play(audio)

echo_command = ["echo", "Hallo dit is een test die ik doe naar tekst naar spraak."]
piper_speaker =  0 #[0,7,8,17,20,40,41,42,44,45,49,50,51]  
piper_command = ["piper", "-m", "nl_NL-mls-medium.onnx", "-s", str(piper_speaker), "-f", "soundbyte.wav"]
echo_process = subprocess.Popen(echo_command, stdout=subprocess.PIPE, shell=True)
piper_process = subprocess.Popen(piper_command, stdin=echo_process.stdout)
echo_process.wait()
piper_process.wait()
audio = pydub.AudioSegment.from_file("soundbyte.wav", format="wav")
play(audio)