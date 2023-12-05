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


all90 = Position(90, 90, 90, 90, 90, 90, 90, 90, 90)
rest = Position(conf.eyeLeft.defaultRotation, conf.eyeRight.defaultRotation, conf.eyeLeftOpen.defaultRotation, conf.eyeRightOpen.defaultRotation, conf.eyesUpDown.defaultRotation, conf.mouth.defaultRotation, conf.headTilt.defaultRotation, conf.headSwivel.defaultRotation, conf.headPivot.defaultRotation)
closeEyes = Position(conf.eyeLeft.minRotation, conf.eyeRight.maxRotation, None, None, None, None, None, None, None)
openEyes = Position(conf.eyeLeft.maxRotation, conf.eyeRight.minRotation, None, None, None, None, None, None, None)
