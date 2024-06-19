import os
import asyncio
import sys

import sound_driver.sound_driver.sound_driver as sound_driver
import speech_driver.speech_driver.speech_driver as speech_driver
import message_hub.message_hub.message_hub as message_hub

async def sound():
    print("Sound driver running.")
    await sound_driver.main()

async def speech():
    print("Speech driver running.")
    await speech_driver.main()

async def servo():
    print("Servo driver running.")
    await servo_driver.main()

async def hub():
    print("Hub driver running.")
    await message_hub.main()

async def main():
    if os.name == "nt":
        servo_toggle = "no"
    else:
        servo_toggle = input("Run with servomotors? (y/n) Only works on microcontrollers, defaults to no.")
    if servo_toggle == "y" or servo_toggle == "yes":
        import servo_driver.servo_driver.servo_driver as servo_driver
    while True:
        if servo_toggle == "y" or servo_toggle == "yes":
            await asyncio.gather(sound(), servo(), hub(), speech())
        else:
            await asyncio.gather(sound(), hub(), speech())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)