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
        expects body to be formatted as 'speak:{text}'
        checks device type to appropriately call piper through command line using invoke package
        sends a message back to message_hub with the duration of the to-be-spoken text, so the servo_driver can act accordingly.
    """
    connection = await aio_pika.connect_robust("localhost")    

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        audio_queue = await channel.declare_queue("audio_output", auto_delete=True)
    
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print("Message received! " + message.body)
                instructions = message.body.split(":")
                if queue.name in message.body.decode():
                    break
    
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # channel = connection.channel()
    # channel.queue_declare(queue="audio_output")
    # channel.queue_declare(queue="hub")
    
    def callback(ch, method, properties, body):
        print("Message received! " + body.decode())
        instructions = body.decode().split(":")
        if len(instructions) != 2:
            raise Exception("Invalid instructions sent to audio driver - instructions formatted wrong.")
        if instructions[0] == "speak":
            if config.speechSynthesizer == "piper":
                if os.name == "nt":
                    command = "echo " + instructions[1] + " | piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
                else:
                    command = "echo " + instructions[1] + " | ./piper -m nl_NL-mls-medium.onnx -s " + str(config.piperVoice) + " -f soundbyte.wav"
                run(command, hide=True, warn=True)
                audio = AudioSegment.from_file("soundbyte.wav", format="wav")
                duration = librosa.get_duration(path="soundbyte.wav")
                durationMs = round(duration * 10)
                channel.basic_publish(exchange="", routing_key="hub", body="talk:" + str(durationMs))
                play(audio)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue="audio_output", on_message_callback=callback)

    channel.start_consuming()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
