import aio_pika
import asyncio

async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        print("Message received: " + message.body.decode())


async def main() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue("test", auto_delete=True)
        
        await queue.consume(process_message)
        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await connection.close()
        

if __name__ == "__main__":
    asyncio.run(main())