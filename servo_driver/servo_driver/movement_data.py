from dataclasses import dataclass
from typing import Optional

import servo_config as conf


@dataclass
class Position:
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
    eyeLeft=conf.eyeLeft.minRotation,
    eyeRight=conf.eyeRight.maxRotation,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
openEyes = Position(
    eyeLeft=conf.eyeLeft.maxRotation,
    eyeRight=conf.eyeRight.minRotation,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=None,
    headPivot=None
)
laughingEyeRoll = Position(
    eyeLeft=110,
    eyeRight=70,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=70,
    mouth=None,
    headTilt=120,
    headSwivel=None,
    headPivot=None
)
laughingPosition1 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=90,
    headTilt=130,
    headSwivel=None,
    headPivot=None
)
laughingPosition2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=70,
    headTilt=115,
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
    headTilt=80,
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
    headTilt=130,
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
    headSwivel=110,
    headPivot=None
)
shakingNo2 = Position(
    eyeLeft=None,
    eyeRight=None,
    eyeLeftOpen=None,
    eyeRightOpen=None,
    eyesUpDown=None,
    mouth=None,
    headTilt=None,
    headSwivel=80,
    headPivot=None
)
