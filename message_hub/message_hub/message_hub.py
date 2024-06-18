import pika
import os
import sys
import asyncio

async def main():
    """
    Message hub receives messages from different parts of the application, then forwards those messages to appropriate parts.
    """
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hub")
    channel.queue_declare(queue="servo")
    channel.queue_declare(queue="audio_output")
    
    def callback(ch, method, properties, body):
        """
        callback() uses the standard RabbitMQ protocol, then decides where to send the message, and formats it accordingly.
        expects body to be formatted as '{command}:{details}'. Example: 'speak:10', where 10 is the amount of deciseconds (0.1 of a second).
        """
        
        instructions = body.decode().split(":")
        if len(instructions) != 2:
            raise Exception("Invalid instructions sent to hub - instructions formatted wrong.")
        if instructions[0] == "speak":
            channel.basic_publish(exchange="", routing_key="audio_output", body="speak:" + instructions[1])
        elif instructions[0] == "move":
            channel.basic_publish(exchange="", routing_key="servo", body=instructions[1])
        elif instructions[0] == "talk":
            channel.basic_publish(exchange="", routing_key="servo", body="speak:" + instructions[1])
        else:
            raise Exception("Invalid instructions sent to hub.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue="hub", on_message_callback=callback)
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