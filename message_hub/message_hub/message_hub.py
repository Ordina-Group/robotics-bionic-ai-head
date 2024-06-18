import pika
import os
import sys
import asyncio
import aio_pika

channel = None

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
        print("Hub: Message received: " + message.body.decode())
        instructions = message.body.decode().split(":")
        if len(instructions) != 2:
            raise Exception("Invalid instructions sent to hub - instructions formatted wrong.")
        if instructions[0] == "speak":
            reply = "speak:" + instructions[1]
            await publish(reply, "audio_output")
        elif instructions[0] == "move":
            reply = instructions[1]
            await publish(reply, "servo")
        elif instructions[0] == "talk":
            reply = "speak:" + instructions[1]
            await publish(reply, "servo")
        else:
            raise Exception("Invalid instructions sent to hub.")

async def main():
    """
    Message hub receives messages from different parts of the application, then forwards those messages to appropriate parts.
    """
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")
    async with connection:
        global channel 
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        hub_queue = await channel.declare_queue("hub", auto_delete=False)
    
        await hub_queue.consume(callback)
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