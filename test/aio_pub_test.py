import asyncio
import aio_pika

async def publish(message, key):
    await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=key)

async def main() -> None:
    global connection
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost",
    )

    async with connection:
        routing_key = "test"
        
        global channel
        channel = await connection.channel()

        await publish("Hallo", routing_key)
    
    
    async with connection:
        routing_key = "test"
        
        channel = await connection.channel()

        await publish("Hallo", routing_key)

if __name__ == "__main__":
    asyncio.run(main())