import os

import sound_driver.sound_driver.sound_driver as sound_driver
import speech_driver.speech_driver.speech_driver as speech_driver
import message_hub.message_hub.message_hub as message_hub
servo_toggle = input("Run with servomotors? (y/n) Only works on microcontrollers, defaults to no.")
if servo_toggle == "y" or servo_toggle == "yes":
    import servo_driver.servo_driver.servo_driver as servo_driver
