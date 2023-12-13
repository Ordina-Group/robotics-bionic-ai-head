import os
import pika
import sys
import servo_config
from adafruit_servokit import ServoKit
import movement_data
from dataclasses import dataclass, fields
import asyncio


async def main():
    kit = ServoKit(channels=16)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='servo')

    def callback(ch, method, properties, body):
        # instructions = body.decode().split(',')
        # print(f" [x] Received {instructions}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def move(pos):
        i = 0
        for field in fields(pos):
            angle = getattr(pos, field.name)
            if angle is not None:
                kit.servo[i].angle = angle
            i += 1

    def rest():
        move(movement_data.rest)

    def close_eyes():
        move(movement_data.closeEyes)

    def open_eyes():
        move(movement_data.openEyes)

    def all90():
        move(movement_data.all90)

    async def nod_yes():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.noddingYes1)
            await asyncio.sleep(0.4)
            move(movement_data.noddingYes2)
            await asyncio.sleep(0.4)
        open_eyes()

    async def shake_no():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.shakingNo1)
            await asyncio.sleep(0.4)
            move(movement_data.shakingNo2)
            await asyncio.sleep(0.4)
        open_eyes()

    async def blink():
        close_eyes()
        await asyncio.sleep(0.25)
        open_eyes()

    async def laugh():
        rest()
        await asyncio.sleep(0.1)
        move(movement_data.laughingEyeRoll)
        await asyncio.sleep(0.2)
        close_eyes()
        i = 0
        while i < 8:
            move(movement_data.laughingPosition1)
            await asyncio.sleep(0.2)
            move(movement_data.laughingPosition2)
            await asyncio.sleep(0.2)
            i += 1
        rest()

    def manual(servo_number, angle):
        kit.servo[servo_number].angle = angle

    async def configure(servo_number):
        i = 0
        while i < 2:
            kit.servo[servo_number].angle = 80
            await asyncio.sleep(0.5)
            kit.servo[servo_number].angle = 110
            await asyncio.sleep(0.5)
            i += 1
        kit.servo[servo_number].angle = 90

    channel.basic_consume(queue='servo', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
