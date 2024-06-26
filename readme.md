# Welcome to the repository for Ordina's application for the YouBionic robot head. <br>
You can find a tutorial to get you started in the Teams-environment! :) <br>
If you don't want to have a visual tutorial, you can find a written one at the bottom of this readme.md <br>
Once you have that going, open a command line interface like Bash, Powershell or CMD, navigate to the folder and run `__main__.py`.
<br>

# What it does <br>
This application is designed to be used on a microcontroller like a Raspberry Pi, in combination with the (adjusted version of the) YouBionic Robot Head, the Adafruit PCA9685, the ReSpeaker Mic Array and a device that outputs audio, like the JBL Go.
The robot starts out in 'sleep mode', waiting for a user to say the Wake Word out loud (which is "robot"). Once awake, the robot will listen to further voice input, decide how to respond, and either talk back or perform the desired action.

> The robot head _**only accepts Dutch**_ voice input.

# Current features <br>
Currently, the robot can
* Answer certain questions
* Tell a joke
* Tell a fun fact
* Laugh at your jokes

# Application structure <br>
This application is split up in a few different parts: <br>
* Message_hub
* Servo_driver
* Sound_driver
* Speech_driver

## Message_hub <br>
This package is the central hub through which communication happens. It receives messages on the "hub" RabbitMQ queue, and forwards them to appropriate components

## Servo_driver <br>
This package controls the servomotors that make the head move. It accepts a few commands, all documented within the code with DocStrings. Inside the package you will find configuration for the servomotors as well as classes that represent different facial expressions and position of the 'muscles' of the robot. The package listens to the "servo" RabbitMQ queue.

## Sound_driver <br>
This package creates audio files using a speech synthesis package - currently PiperTTS. It listens to the "audio_output" RabbitMQ queue, and creates and plays an audio file depending on the text received.

## Speech_driver <br>
This package listens to the user's voice input. It also controls a lot of the decisionmaking, due to the nature of speech controls. The package is configurable to use different speech recognition implementations like Whisper, Wit or VOSK. Inside the package you will find files to configure what the robot will reply to certain commands, as well as a list of jokes and fun facts it can tell. Depending on the configuration, the robot can return hardcoded replies, or generate new ones using the Fietje 2B LLM model by Bram Vanroy. 

## Installation <br>
Start by getting a clean microcontroller such as a Raspberry Pi. Flash Raspberry OS to an empty SD-card, and proceed by installing the Pi. <br>
Once the Pi is all set up, make sure your device has the following folders: -Desktop -Downloads -Documents. Then navigate to this GitHub environment. You will find a .txt file called "install_scripts.txt". <br>
Copy the contents of the install scripts up until the dotted line ( -------- ). Paste the text into your favourite commandline interface such as Bash.
This will take a while. Let it run while you go grab yourself a coffee or do some research in the meantime. <br>
Once the command is done, run `sudo raspi-config`. Navigate to Interface Options -> I2C. Enable it, then finish. <br>
Almost done! Navigate to 'sound-driver/sound-driver/' and put all contents from 'Downloads/piper[version].tar.gz' in there. <br>
Navigate to 'speech-driver/' and create a new folder called `vosk`. Put the contents from 'Downloads/vosk-model[version].zip' there in separate folders. You should now have 'speech-driver/vosk/[different-models]' and 'speech-driver/speech-driver/' <br>
And that's it! Unless you wish to use `Wit.ai`, an online speech/intent recognition package. If that's the case, create a new project on Wit.ai, copy your developer key, and paste it in a file called `witkey.txt`, located in the same folder as `__main__.py`. <br>
Good luck! 
