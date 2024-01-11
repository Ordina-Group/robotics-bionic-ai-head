from dataclasses import dataclass


@dataclass
class ServoMotor:
    pinNr: int
    defaultRotation: int
    minRotation: int
    maxRotation: int
    name: str


eyeLeft = ServoMotor(pinNr=0, defaultRotation=100, minRotation=80, maxRotation=115, name='eyeLeft')
eyeRight = ServoMotor(pinNr=1, defaultRotation=100, minRotation=80, maxRotation=115, name='eyeRight')
eyeLeftOpen = ServoMotor(pinNr=2, defaultRotation=100, minRotation=80, maxRotation=120, name='eyeLeftOpen')
eyeRightOpen = ServoMotor(pinNr=3, defaultRotation=100, minRotation=80, maxRotation=120, name='eyeRightOpen')
eyesUpDown = ServoMotor(pinNr=4, defaultRotation=105, minRotation=70, maxRotation=180, name='eyesUpDown')
mouth = ServoMotor(pinNr=5, defaultRotation=70, minRotation=70, maxRotation=100, name='mouth')
headTilt = ServoMotor(pinNr=13, defaultRotation=110, minRotation=70, maxRotation=150, name='headTilt')
headSwivel = ServoMotor(pinNr=14, defaultRotation=95, minRotation=50, maxRotation=130, name='headSwivel')
headPivot = ServoMotor(pinNr=15, defaultRotation=95, minRotation=70, maxRotation=110, name='headPivot')
