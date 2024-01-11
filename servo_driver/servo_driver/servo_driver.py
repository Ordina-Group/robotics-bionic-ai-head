import os
import pika
import sys
import servo_config as config
from adafruit_servokit import ServoKit
import movement_data
from dataclasses import dataclass, fields, asdict
# import asyncio
# import aio_pika
# I have these commented out, as to indicate a desire to make everything asynchronous. This way, the head can move more naturally. As for now, it's a sequential driver, as I'm struggling to understand asynchronity.


def main():
    kit = ServoKit(channels=16)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='servo')
    
    def move(pos):
        for field, value in asdict(pos).items:
            if value is not None:
                pinNumber = findPinNumber(field)
                kit.servo[pinNumber].angle = value

    def rest():
        move(movement_data.rest)

    def close_eyes():
        move(movement_data.closeEyes)

    def open_eyes():
        move(movement_data.openEyes)

    def all90():
        move(movement_data.all90)

    def nod_yes():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.noddingYes1)
            sleep(0.4)
            move(movement_data.noddingYes2)
            sleep(0.4)
        open_eyes()

    def shake_no():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.shakingNo1)
            sleep(0.4)
            move(movement_data.shakingNo2)
            sleep(0.4)
        open_eyes()

    def blink():
        close_eyes()
        sleep(0.25)
        open_eyes()

    def laugh():
        rest()
        sleep(0.1)
        move(movement_data.laughingEyeRoll)
        sleep(0.2)
        close_eyes()
        i = 0
        while i < 8:
            move(movement_data.laughingPosition1)
            sleep(0.2)
            move(movement_data.laughingPosition2)
            sleep(0.2)
            i += 1
        rest()

    def manualWithName(servoName, angle):
        servo_number = findPinNumber(servoName)
        kit.servo[servo_number].angle = angle

    def manualWithNumber(servo_number, angle):
        kit.servo[servo_number].angle = angle

    def configure(servo_number):
        i = 0
        while i < 2:
            kit.servo[servo_number].angle = 80
            sleep(0.5)
            kit.servo[servo_number].angle = 110
            sleep(0.5)
            i += 1
        kit.servo[servo_number].angle = 90
    
    def speak(text):
        # If the robot head were to ever speak, this method would make that happen. 
        # However, as this is outside of the scope of this current assignment,
        # it is just an empty method for now.
        sleep(2)
        
    def findPinNumber(servoMotorName):
        servoMotors = [config.eyeLeft, config.eyeRight, config.eyeLeftOpen, config.eyeRightOpen, config.eyesUpDown, config.mouth, config.headTilt, config.headSwivel, config.headPivot]
        for servoMotor in servoMotors:
            if servoMotorName == servoMotor.name:
                return servoMotor.pinNr
    
    # Here we define what possible commands can be sent to the driver.
    # If future developers add new methods, make sure to add them to this dictionary.
    commands = {
        'rest': rest,
        'close_eyes': close_eyes,
        'open_eyes': open_eyes,
        'all90': all90,
        'nod_yes': nod_yes,
        'shake_no': shake_no,
        'blink': blink,
        'laugh': laugh
    }
    
    def callback(ch, method, properties, body):
        instructions = body.decode().split(':')
        print(f" [x] Received {instructions}")
        if instructions[0] == "speak":
            speak(instructions[1])
        elif instructions[0] in commands:
            commands[instructions[0]]()
        elif instructions[0] == "manualWithName":
            manualWithName(instructions[1], instructions[2])
        elif instructions[0] == "manualWithNumber":
            manualWithNumber(instructions[1], instructions[2])
        elif instructions[0] == "config":
            config(instructions[1])
        else:
            print("Unknown command: %s" % (instructions[0]))
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
