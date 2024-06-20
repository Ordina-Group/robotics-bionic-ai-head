import os
import pika
import sys
import numpy
import time
from pydub import AudioSegment
from pydub.playback import play
from invoke import run
import sound_driver.sound_driver.config as config
import librosa
import asyncio
import aio_pika


async def main():
    """
    Class used to control the sound output. Requires the hardware to be connected in any way to a speaker or similiar device.
    
    ...
    
    Methods:
    --------
    callback(ch, method, properties, body):
        default RabbitMQ callback method used for communication.
        expects body to be formatted as 'speak:::{text}'
        checks device type to appropriately call piper through command line using invoke package
        sends a message back to message_hub with the duration of the to-be-spoken text, so the servo_driver can act accordingly.
    """
    
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")    

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        audio_queue = await channel.declare_queue("audio_output", auto_delete=False)
    
        def play_audio_sync(audio):
            play(audio)
        
        async def play_audio(path, file_type):
            if os.name == "nt":
                audio = AudioSegment.from_file("sound_driver\\sound_driver\\soundbyte.wav", format="wav")
            else:
                audio = AudioSegment.from_file("./sound_driver/sound_driver/soundbyte.wav", format="wav")
            await asyncio.to_thread(play, audio)
            return

        async def run_command(command):
            run(command, hide=True, warn=True)
            return

        async def publish(message, routing_key):
            print("Audio: Message sent!: " + message)
            await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
            return

        async def callback(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process(ignore_processed=True):
                await message.ack()
                print("Audio: Message received: " + message.body.decode())
                instructions = message.body.decode().split(":::")
                if len(instructions) != 2:
                    raise Exception("Invalid instructions sent to audio driver - instructions formatted wrong.")
                if instructions[0] == "speak":
                    if config.speechSynthesizer == "piper":
                        stripped_instructions = instructions[1].strip()
                        split_instructions = stripped_instructions.split()
                        joined_instructions = " ".join(split_instructions)
                        clean_instructions = joined_instructions.replace(".", "").replace("?", "").replace("!", "")
                        if os.name == "nt":
                            command = "echo " + clean_instructions + " | sound_driver\\sound_driver\\piper -m sound_driver\\sound_driver\\nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f sound_driver\\sound_driver\\soundbyte.wav"
                        else:
                            command = "echo " + clean_instructions + " | ./sound_driver/sound_driver/piper -m ./sound_driver/sound_driver/nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f ./sound_driver/sound_driver/soundbyte.wav"
                        await run_command(command)
                        path = "sound_driver/sound_driver/soundbyte.wav"
                        duration = librosa.get_duration(path=path)
                        durationMs = round(duration * 10)
                        reply = "talk:::" + str(durationMs)
                        await publish(reply, "hub")
                        pause_reply = "pause:::" + str(durationMs)
                        await publish(pause_reply, "hub")
                        await play_audio(path, "wav")
    
        await audio_queue.consume(callback)
        try:
            await asyncio.Future()
        finally:
            await connection.close()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
