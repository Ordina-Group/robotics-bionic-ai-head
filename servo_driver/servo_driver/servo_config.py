from dataclasses import dataclass


@dataclass
class ServoMotor:
    pinNr: int
    defaultRotation: int
    minRotation: int
    maxRotation: int


eyeLeft = ServoMotor(pinNr=0, defaultRotation=100, minRotation=80, maxRotation=115)
eyeRight = ServoMotor(pinNr=1, defaultRotation=100, minRotation=80, maxRotation=115)
eyeLeftOpen = ServoMotor(pinNr=2, defaultRotation=100, minRotation=80, maxRotation=120)
eyeRightOpen = ServoMotor(pinNr=3, defaultRotation=100, minRotation=80, maxRotation=120)
eyesUpDown = ServoMotor(pinNr=4, defaultRotation=105, minRotation=70, maxRotation=180)
mouth = ServoMotor(pinNr=5, defaultRotation=70, minRotation=70, maxRotation=100)
headTilt = ServoMotor(pinNr=13, defaultRotation=110, minRotation=70, maxRotation=150)
headSwivel = ServoMotor(pinNr=14, defaultRotation=95, minRotation=50, maxRotation=130)
headPivot = ServoMotor(pinNr=15, defaultRotation=95, minRotation=70, maxRotation=110)
