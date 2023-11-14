from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[0].angle=0
kit.servo[1].angle=0
kit.servo[2].angle=0
kit.servo[3].angle=0
kit.servo[4].angle=0
kit.servo[15].angle=0
time.sleep(1)
kit.servo[0].angle=180
time.sleep(0.1)
kit.servo[1].angle=180
time.sleep(0.1)
kit.servo[2].angle=180
time.sleep(0.1)
kit.servo[3].angle=180
time.sleep(0.1)
kit.servo[4].angle=180
time.sleep(0.1)
kit.servo[15].angle=180
time.sleep(1)
kit.servo[0].angle=0
kit.servo[1].angle=0
kit.servo[2].angle=0
kit.servo[3].angle=0
kit.servo[4].angle=0
kit.servo[15].angle=0
quit()
