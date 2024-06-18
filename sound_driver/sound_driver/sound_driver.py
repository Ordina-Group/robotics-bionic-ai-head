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

channel = None

async def run_command(command):
    run(command, hide=True, warn=True)
    return

async def publish(message, routing_key):
    connection = await aio_pika.connect("amqp://guest:guest@localhost")
    async with connection:
        temp_channel = await connection.channel()
        await temp_channel.set_qos(prefetch_count=10)
        temp_queue = await temp_channel.declare_queue(routing_key, auto_delete=False)
        await temp_channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
        return

async def callback(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process(ignore_processed=True):
        await message.ack()
        print("Audio: Message received: " + message.body.decode())
        instructions = message.body.decode().split(":")
        if len(instructions) != 2:
            raise Exception("Invalid instructions sent to audio driver - instructions formatted wrong.")
        if instructions[0] == "speak":
            if config.speechSynthesizer == "piper":
                if os.name == "nt":
                    command = "echo " + instructions[1] + " | piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
                else:
                    command = "echo " + instructions[1] + " | ./piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
                await run_command(command)
                audio = AudioSegment.from_file("sound_driver/sound_driver/soundbyte.wav", format="wav")
                duration = librosa.get_duration(path="soundbyte.wav")
                durationMs = round(duration * 10)
                reply = "talk:" + str(durationMs)
                await publish(reply, "hub")
                play(audio)

async def main():
    """
    Class used to control the sound output. Requires the hardware to be connected in any way to a speaker or similiar device.
    
    ...
    
    Methods:
    --------
    callback(ch, method, properties, body):
        default RabbitMQ callback method used for communication.
        expects body to be formatted as 'speak:{text}'
        checks device type to appropriately call piper through command line using invoke package
        sends a message back to message_hub with the duration of the to-be-spoken text, so the servo_driver can act accordingly.
    """
    
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")    

    async with connection:
        global channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        audio_queue = await channel.declare_queue("audio_output", auto_delete=False)
    
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
