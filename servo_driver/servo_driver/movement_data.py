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
    headSwivel=conf.headSwivel.minRotation,
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
    headSwivel=conf.headSwivel.maxRotation,
    headPivot=None
)
sleep = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=conf.eyeLeftOpen.minRotation,
    eyeRightOpen=conf.eyeRightOpen.maxRotation,
    eyesUpDown=conf.eyesUpDown.maxRotation,
    mouth=conf.mouth.minRotation,
    headTilt=conf.headTilt.minRotation,
    headSwivel=None,
    headPivot=None
)
sus = Position(
    eyeLeft=conf.eyeLeft.defaultRotation,
    eyeRight=conf.eyeRight.defaultRotation,
    eyeLeftOpen=(conf.eyeLeftOpen.minRotation + 20),
    eyeRightOpen=(conf.eyeRightOpen.maxRotation - 20),
    eyesUpDown=(conf.eyesUpDown.defaultRotation + 10),
    mouth=conf.mouth.minRotation,
    headTilt=None,
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