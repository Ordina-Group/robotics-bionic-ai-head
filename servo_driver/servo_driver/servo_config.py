from dataclasses import dataclass


@dataclass
class ServoMotor:
    pinNr: int
    defaultRotation: int
    minRotation: int
    maxRotation: int


eyeLeft = ServoMotor(0, 100, 80, 115)
eyeRight = ServoMotor(1, 100, 80, 115)
eyeLeftOpen = ServoMotor(2, 100, 80, 120)
eyeRightOpen = ServoMotor(3, 100, 80, 120)
eyesUpDown = ServoMotor(4, 105, 70, 180)
mouth = ServoMotor(5, 70, 70, 100)
headTilt = ServoMotor(13, 110, 70, 150)
headSwivel = ServoMotor(14, 95, 50, 130)
headPivot = ServoMotor(15, 95, 70, 110)
