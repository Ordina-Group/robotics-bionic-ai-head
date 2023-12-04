import pika, sys, os
from adafruit_servokit import ServoKit

def main():
	kit = ServoKit(channels=16)
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='servo')
	
	def callback(ch, method, properties, body):
		instructions = body.decode().split(',')
		print(f" [x] Received {instructions}")
		amountofinstructions = int(instructions.pop(0))
		override = int(instructions.pop(-1))
		for instruction in range(amountofinstructions):
			servo = int(instructions.pop(0))
			angle = int(instructions.pop(0))
			kit.servo[servo].angle=angle
		ch.basic_ack(delivery_tag=method.delivery_tag)

	
	channel.basic_consume(queue='servo', on_message_callback=callback)
	
	print(' [*] Waiting for messages. To exit, press CTRL+C')
	channel.start_consuming()
	
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

