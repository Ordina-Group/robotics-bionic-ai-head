# Welcome to the repository for Ordina's application for the YouBionic robot head. <br>
You can find a tutorial to get you started in the Teams-environment! :) <br>
Once you have that going, open a command line interface like Bash, Powershell or CMD, navigate to the folder and run `./start.sh`.
To get it to stop, run `./stop.sh`
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
This package listens to the user's voice input. It also controls a lot of the decisionmaking, due to the nature of speech controls. The package is configurable to use different speech recognition implementations like Whisper, Wit or VOSK. It can also be configured to use different Wake Word Detectors such as Porcupine or Snowboy. Inside the package you will find files to configure what the robot will reply to certain commands, as well as a list of jokes and fun facts it can tell. Currently the head does not support response generation through use of an LLM, due to the unfortunately slow hardware that is the Raspberry Pi. 
