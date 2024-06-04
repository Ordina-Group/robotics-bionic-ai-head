from dataclasses import dataclass


@dataclass
class ServoMotor:
    """
    ServoMotor is a configuration class, used to represent the different servo motors used in the robot head.
    
    ...
    
    Attributes
    ----------
    pinNr: int
        an integer corresponding to the signal pins on the Adafruit PCA9685
    defaultRotation: int
        an integer representing the 'resting' position for the servomotor
    minRotation: int
        an integer of how far the servomotor should be able to rotate without risking damage to the plastic
    maxRotation: int
        an integer of how far the servomotor should be able to rotate without risking damage to the plastic
    name: str
        a string representing the position of the servomotor. Example: "eyeLeft" corresponds to the left eye of the head
    """
    
    pinNr: int
    defaultRotation: int
    minRotation: int
    maxRotation: int
    name: str


eyeLeft = ServoMotor(pinNr=2, defaultRotation=105, minRotation=90, maxRotation=120, name="eyeLeft")
eyeRight = ServoMotor(pinNr=3, defaultRotation=80, minRotation=70, maxRotation=100, name="eyeRight")
eyeLeftOpen = ServoMotor(pinNr=1, defaultRotation=100, minRotation=60, maxRotation=110, name="eyeLeftOpen")
eyeRightOpen = ServoMotor(pinNr=0, defaultRotation=90, minRotation=70, maxRotation=120, name="eyeRightOpen")
eyesUpDown = ServoMotor(pinNr=4, defaultRotation=100, minRotation=80, maxRotation=140, name="eyesUpDown")
mouth = ServoMotor(pinNr=5, defaultRotation=40, minRotation=30, maxRotation=80, name="mouth")
headTilt = ServoMotor(pinNr=13, defaultRotation=95, minRotation=70, maxRotation=115, name="headTilt")
headSwivel = ServoMotor(pinNr=14, defaultRotation=110, minRotation=90, maxRotation=130, name="headSwivel")
headPivot = ServoMotor(pinNr=15, defaultRotation=100, minRotation=70, maxRotation=130, name="headPivot")
