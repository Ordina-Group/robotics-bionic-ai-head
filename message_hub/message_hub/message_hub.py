import pika
import os
import sys

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hub")
    channel.queue_declare(queue="servo")
    channel.queue_declare(queue="audio_output")
    
    def callback(ch, method, properties, body):
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
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)