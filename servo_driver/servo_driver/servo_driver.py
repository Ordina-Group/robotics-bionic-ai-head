import os
import pika
import sys
import servo_driver.servo_driver.servo_config as servo_config
from random import choice
from adafruit_servokit import ServoKit
import servo_driver.servo_driver.movement_data as movement_data
from dataclasses import dataclass, fields, asdict
import time
import asyncio
import aio_pika


async def main():
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
    
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")    

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        servo_queue = await channel.declare_queue("servo", auto_delete=False)
        
        should_blink = False
        
        kit = ServoKit(channels=16)
        
        def move_sync(pin, angle):
            kit.servo[pin].angle = angle
        
        async def move(pos):
            for field, value in asdict(pos).items():
                if value is not None:
                    servoDetails = findPinNumber(field)
                    if not value < servoDetails[1] and not value > servoDetails[2]:
                        pin = servoDetails[0]
                        angle = value
                        await asyncio.to_thread(move_sync, pin, angle)
                        
        
        async def rest():
            should_blink = True
            await move(movement_data.rest)
        
        async def close_eyes():
            should_blink = False
            await move(movement_data.closeEyes)

        async def open_eyes():
            should_blink = False
            await move(movement_data.openEyes)

        async def all90():
            should_blink = False
            await move(movement_data.all90)

        async def sleep():
            should_blink = False
            await move(movement_data.sleep)

        async def sus():
            should_blink = False
            await move(movement_data.sus)
            should_blink = True

        async def speak(duration):
            should_blink = True
            i = 0
            options = [movement_data.mouthDefault, movement_data.mouthOpen1, movement_data.mouthOpen2, movement_data.mouthOpen3]
            await rest()
            while i < int(duration):
                await move(choice(options))
                await asyncio.sleep(0.1)
                i += 1
            await move(movement_data.mouthShut)
            should_blink = False


        async def nod():
            await close_eyes()
            i = 0
            while i < 5:
                await move(movement_data.noddingYes1)
                await asyncio.sleep(0.4)
                await move(movement_data.noddingYes2)
                await asyncio.sleep(0.4)
                i += 1
            await open_eyes()
            should_blink = True

        async def shake():
            should_blink = False
            await close_eyes()
            i = 0
            while i < 5:
                await move(movement_data.shakingNo1)
                await asyncio.sleep(0.4)
                await move(movement_data.shakingNo2)
                await asyncio.sleep(0.4)
                i += 1
            await open_eyes()
            should_blink = True

        async def blink():
            await close_eyes()
            await asyncio.sleep(0.25)
            await open_eyes()

        async def laugh():
            await rest()
            should_blink = False
            await asyncio.sleep(0.1)
            await move(movement_data.laughingEyeRoll)
            await asyncio.sleep(0.2)
            await close_eyes()
            i = 0
            while i < 11:
                await move(movement_data.laughingPosition1)
                await asyncio.sleep(0.2)
                await move(movement_data.laughingPosition2)
                await asyncio.sleep(0.2)
                i += 1
            await rest()

        async def manualWithName(servoName, angle):
            servo_number = findPinNumber(servoName)
            await asyncio.to_thread(move_sync, servo_number, angle)

        async def manualWithNumber(servo_number, angle):
            await asyncio.to_thread(move_sync, servo_number, angle)

        async def configure(servo_number):
            i = 0
            while i < 2:
                kit.servo[servo_number].angle = 80
                await asyncio.sleep(0.5)
                kit.servo[servo_number].angle = 110
                await asyncio.sleep(0.5)
                i += 1
            kit.servo[servo_number].angle = 90

            
        def findPinNumber(servoMotorName):
            servoMotors = [servo_config.eyeLeft, servo_config.eyeRight, servo_config.eyeLeftOpen, servo_config.eyeRightOpen, servo_config.eyesUpDown, servo_config.mouth, servo_config.headTilt, servo_config.headSwivel, servo_config.headPivot]
            for servoMotor in servoMotors:
                if servoMotorName == servoMotor.name:
                    return servoMotor.pinNr, servoMotor.minRotation, servoMotor.maxRotation
        
        async def takeAction(instructions)
            command = instructions[0]
            if command == "speak":
                await speak(instructions[1])
            elif command == "blink":
                await blink()
            elif command == "rest":
                await rest()
            elif command == "close_eyes":
                await close_eyes()
            elif command == "open_eyes":
                await open_eyes()
            elif command == "all90":
                await all90()
            elif command == "nod":
                await nod()
            elif command == "shake":
                await shake()
            elif command == "laugh":
                await laugh()
            elif command == "sleep":
                await sleep()
            elif command == "sus":
                await sus()
            elif command == "manualWithName":
                await manualWithName(instructions[1], int(instructions[2]))
            elif command == "manualWithNumber":
                await manualWithNumber(int(instructions[1]), int(instructions[2]))
            elif command == "config":
                await configure(int(instructions[1]))
            else:
                print("Unknown command: %s" % (instructions[0]))
            return
        
        
        async def callback(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process(ignore_processed=True):
                await message.ack()
                print("Servo: Message received: " + message.body.decode())
                instructions = message.body.decode().split(":::")
                await takeAction(instructions)
                
                
        
        async def autoblink():
            while True:
                await asyncio.sleep(4)
                if should_blink == True:
                    await blink()
        
        async def consume_queue():
            await servo_queue.consume(callback)
            try:
                await asyncio.Future()
            finally:
                await connection.close() 
        
        await asyncio.gather(autoblink(), consume_queue())

   

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)