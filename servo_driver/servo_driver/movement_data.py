from dataclasses import dataclass
from typing import Optional

import servo_config as conf


@dataclass
class Position:
    """
    A class used to represent a 'facial expression' for the head.
    Each instance is a certain position all the servomotors should rotate to.
    Generally  these are dependent on the servo_configs minRotation and maxRotation.
    
    ...
    
    Attributes
    ----------
    eyeLeft: Optional[int]
        an optional integer between 0 and 180 representing the left eye's rotation - goes left to right.
    eyeRight: Optional[int]
        an optional integer between 0 and 180 representing the right eye's rotation - goes left to right.
    eyeLeftOpen: Optional[int]
        an optional integer between 0 and 180 representing how far the left eye is opened.
    eyeRightOpen: Optional[int]
        an optional integer between 0 and 180 representing how far the right eye is opened.
    eyesUpDown: Optional[int]
        an optional integer between 0 and 180 representing how far both eyes are pointing up or down.
    mouth: Optional[int]
        an optional integer between 0 and 180 representing how far the jaw gets opened.
    headTilt: Optional[int]
        an optional integer between 0 and 180 representing how far the head looks up or down.
    headSwivel: Optional[int]
        an optional integer between 0 and 180 representing how far the head looks left or right.
    headPivot: Optional[int]
        an optional integer between 0 and 180 representing how far the head is angled diagonally, like puppies do.
    """
    
    eyeLeft: Optional[int]
    eyeRight: Optional[int]
    eyeLeftOpen: Optional[int]
    eyeRightOpen: Optional[int]
    eyesUpDown: Optional[int]
    mouth: Optional[int]
    headTilt: Optional[int]
    headSwivel: Optional[int]
    headPivot: Optional[int]


all90 = Position(
    eyeLeft=90,
    eyeRight=90,
    eyeLeftOpen=90,
    eyeRightOpen=90,
    eyesUpDown=90,
    mouth=90,
    headTilt=90,
    headSwivel=90,
    headPivot=90
)
rest = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=conf.eyeLeftOpen.defaultRotation,
    eyeRightOpen=conf.eyeRightOpen.defaultRotation,
    eyesUpDown=conf.eyesUpDown.defaultRotation,
    mouth=conf.mouth.defaultRotation,
    headTilt=conf.headTilt.defaultRotation,
    headSwivel=conf.headSwivel.defaultRotation,
    headPivot=conf.headPivot.defaultRotation
)
closeEyes = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=conf.eyeLeftOpen.minRotation,
    eyeRightOpen=conf.eyeRightOpen.maxRotation,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
openEyes = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=conf.eyeLeftOpen.defaultRotation,
    eyeRightOpen=conf.eyeRightOpen.defaultRotation,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
laughingEyeRoll = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=conf.eyesUpDown.minRotation,
    mouth=None,
    headTilt=conf.headTilt.maxRotation,
    headSwivel=None,
    headPivot=None
)
laughingPosition1 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=conf.mouth.defaultRotation,
    headTilt=conf.headTilt.maxRotation,
    headSwivel=None,
    headPivot=None
)
laughingPosition2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=(conf.mouth.defaultRotation + 20),
    headTilt=(conf.headTilt.maxRotation - 10),
    headSwivel=None,
    headPivot=None
)
noddingYes1 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=conf.headTilt.minRotation,
    headSwivel=None,
    headPivot=None
)
noddingYes2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=conf.headTilt.maxRotation,
    headSwivel=None,
    headPivot=None
)
shakingNo1 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=conf.headPivot.minRotation
)
shakingNo2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=conf.headPivot.maxRotation
)
sleep = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=conf.eyeLeftOpen.minRotation,
    eyeRightOpen=conf.eyeRightOpen.maxRotation,
    eyesUpDown=conf.eyesUpDown.maxRotation,
    mouth=conf.mouth.minRotation,
    headTilt=conf.headTilt.minRotation,
    headSwivel=conf.headSwivel.defaultRotation,
    headPivot=conf.headPivot.defaultRotation
)
sus = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=(conf.eyeLeftOpen.minRotation + 20),
    eyeRightOpen=(conf.eyeRightOpen.maxRotation - 20),
    eyesUpDown=(conf.eyesUpDown.defaultRotation + 10),
    mouth=conf.mouth.minRotation,
    headTilt=conf.headTilt.defaultRotation,
    headSwivel=(conf.headSwivel.minRotation + 10),
    headPivot=(conf.headPivot.minRotation + 10)
)
mouthOpen1 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=(conf.mouth.defaultRotation + 10),
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
mouthOpen2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=(conf.mouth.defaultRotation + 20),
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
mouthOpen3 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=(conf.mouth.defaultRotation + 30),
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
mouthShut = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=conf.mouth.minRotation,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
mouthDefault = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=conf.mouth.defaultRotation,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)