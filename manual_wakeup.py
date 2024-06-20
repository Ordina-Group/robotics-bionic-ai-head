import asyncio
import aio_pika
import sys
import os

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")    
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        
        async def publish(message, routing_key="audio_input"):
            print("Wakeup sent!")
            message = "wakeup"
            await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
            return
        
        while True:
            message = input("Send wakeup signal? Send 'sleep' for sleep, 'pause' for pause, defaults to 'wakeup'")
            if message == "sleep":
                await publish("sleep")
                await publish("move:::sleep", "hub")
            elif message == "pause":
                duration = input("for how long?")
                await publish("pause:::" + str(duration))
            else:
                await publish("wakeup")
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)