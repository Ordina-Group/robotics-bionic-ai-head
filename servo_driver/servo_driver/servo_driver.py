import os
import pika
import sys
import servo_driver.servo_driver.servo_config as servo_config
from random import choice
from adafruit_servokit import ServoKit
import servo_driver.servo_driver.movement_data
from dataclasses import dataclass, fields, asdict
import time
# import asyncio
# import aio_pika

def main():
    """
    Class to control the servomotors. 
    
    ...
    
    Methods
    -------
    move(pos)
        moves a servomotor to a certain angle, depending on the dictionary passed to it.
        is frequently called by other methods in the class to perform the movement itself
        
        Parameters
        ----------
        pos: dict(field: string, value: integer)
            represents a servomotor, called by its name as detailed in servo_config.py, the integer is the desired angle
    -----------            
    rest()
        moves all servomotors to their default position
    close_eyes()
        sends a signal to move corresponding servomotors to close the robot's eyes.
    open_eyes()
        sends a signal to move corresponding servomotors to open the robot's eyes.
    all_90()
        sends a signal to all servomotors to be positioned in a 90 degree angle. Only used during assembly of the robot, as all servomotors need to be angled correctly before assembly.
    sleep()
        sends a signal to all servomotors to move to predetermined sleeping position.
    sus()
        sends a signal to all servomotors to move to predetermined 'sus' position. Used to signal the robot is thinking.
    speak(duration: int)
        makes the robots mouth move for duration (in deciseconds - 0.1 of a second) to make it look like the robot is talking. Makes the eyes blink every 0.8 seconds.
    nod()
        sends a signal to the corresponding servomotors to let the head 'nod' yes, as if agreeing with something.
    shake()
        sends a signal to the corresponding servomotors to let the head 'shake' no, as if disagreeing with something.
    blink()
        sends a signal to rapidly close then open the robot's eyes.
    laugh()
        sends a signal to the corresponding servomotors to appear laughing.
    manualWithName(servoName: string, angle: int)
        moves servomotor with corresponding name to corresponding angle. Used for debugging.
    manualWithnumber(servo_number: int, angle: int)
        moves servomotor with pinNr equal to servo_number to corresponding angle. Used for debugging.
    configure(servo_number: int):
        moves servomotor with corresponding pinNr back and forth. Used for debugging and finding out which servomotor does what.
    findPinNumber(servoMotorName: string)
        looks through the config file to find what pin number corresponds to servomotor with corresponding name.
    callback(ch, method, properties, body):
        default RabbitMQ callback method for communicating. 
    """
    
    kit = ServoKit(channels=16)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="servo")
    
    def move(pos):
        for field, value in asdict(pos).items():
            if value is not None:
                servoDetails = findPinNumber(field)
                if not value < servoDetails[1] and not value > servoDetails[2]:
                    kit.servo[servoDetails[0]].angle = value

    def rest():
        move(movement_data.rest)

    def close_eyes():
        move(movement_data.closeEyes)

    def open_eyes():
        move(movement_data.openEyes)

    def all90():
        move(movement_data.all90)

    def sleep():
        move(movement_data.sleep)

    def sus():
        move(movement_data.sus)

    def speak(duration):
        i = 0
        options = [movement_data.mouthDefault, movement_data.mouthOpen1, movement_data.mouthOpen2, movement_data.mouthOpen3]
        rest()
        while i < int(duration):
            if i % 8 == 0: 
                close_eyes()
                time.sleep(0.1)
                move(choice(options))
                time.sleep(0.1)
                open_eyes()
                time.sleep(0.1)
                i += 3
            else:
                move(choice(options))
                time.sleep(0.1)
                i += 1
        move(movement_data.mouthShut)

    def nod():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.noddingYes1)
            time.sleep(0.4)
            move(movement_data.noddingYes2)
            time.sleep(0.4)
            i += 1
        open_eyes()

    def shake():
        close_eyes()
        i = 0
        while i < 5:
            move(movement_data.shakingNo1)
            time.sleep(0.4)
            move(movement_data.shakingNo2)
            time.sleep(0.4)
            i += 1
        open_eyes()

    def blink():
        close_eyes()
        time.sleep(0.25)
        open_eyes()

    def laugh():
        rest()
        time.sleep(0.1)
        move(movement_data.laughingEyeRoll)
        time.sleep(0.2)
        close_eyes()
        i = 0
        while i < 11:
            move(movement_data.laughingPosition1)
            time.sleep(0.2)
            move(movement_data.laughingPosition2)
            time.sleep(0.2)
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
            time.sleep(0.5)
            kit.servo[servo_number].angle = 110
            time.sleep(0.5)
            i += 1
        kit.servo[servo_number].angle = 90

        
    def findPinNumber(servoMotorName):
        servoMotors = [servo_config.eyeLeft, servo_config.eyeRight, servo_config.eyeLeftOpen, servo_config.eyeRightOpen, servo_config.eyesUpDown, servo_config.mouth, servo_config.headTilt, servo_config.headSwivel, servo_config.headPivot]
        for servoMotor in servoMotors:
            if servoMotorName == servoMotor.name:
                return servoMotor.pinNr, servoMotor.minRotation, servoMotor.maxRotation
    
    # Here we define what possible commands can be sent to the driver.
    # If future developers add new methods, make sure to add them to this dictionary.
    commands = {
        "rest": rest,
        "close_eyes": close_eyes,
        "open_eyes": open_eyes,
        "all90": all90,
        "nod": nod,
        "shake": shake,
        "blink": blink,
        "laugh": laugh,
        "demo": demo,
        "sleep": sleep,
        "sus": sus
    }
    
    def callback(ch, method, properties, body):
        instructions = body.decode().split(":")
        print(f" [x] Received {instructions}")
        if instructions[0] == "speak":
            speak(instructions[1])
        elif instructions[0] in commands:
            commands[instructions[0]]()
        elif instructions[0] == "manualWithName":
            manualWithName(instructions[1], int(instructions[2]))
        elif instructions[0] == "manualWithNumber":
            manualWithNumber(int(instructions[1]), int(instructions[2]))
        elif instructions[0] == "config":
            configure(int(instructions[1]))
        else:
            print("Unknown command: %s" % (instructions[0]))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue="servo", on_message_callback=callback)

    print(" [*] Waiting for messages. To exit, press CTRL+C")
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
