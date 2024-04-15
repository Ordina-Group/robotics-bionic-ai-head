from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
	
def move(servo, angle):
	kit.servo[servo].angle = angle
	
while True:
	servo = input("Enter servonumber to be calibrated: ")
	angle = input("Enter angle: ")
	move(int(servo), int(angle))
