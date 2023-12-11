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


# TODO: Wanneer alle posities hier staan kan er een functie geschreven worden die
# TODO: ervoor zorgt dat per pose alle values worden opgehaald en de servo's
# TODO: worden aangestuurd daarmee. Dan kan je per servo vanaf de config de pinnr halen
# TODO: en de rotaties hieruit halen. Als er 'None' staat, hoeft de servo niet te bewegen
all90 = Position(90, 90, 90, 90, 90, 90, 90, 90, 90)
rest = Position(conf.eyeLeft.defaultRotation, conf.eyeRight.defaultRotation, conf.eyeLeftOpen.defaultRotation, conf.eyeRightOpen.defaultRotation, conf.eyesUpDown.defaultRotation, conf.mouth.defaultRotation, conf.headTilt.defaultRotation, conf.headSwivel.defaultRotation, conf.headPivot.defaultRotation)
closeEyes = Position(conf.eyeLeft.minRotation, conf.eyeRight.maxRotation, None, None, None, None, None, None, None)
openEyes = Position(conf.eyeLeft.maxRotation, conf.eyeRight.minRotation, None, None, None, None, None, None, None)
laughingEyeRoll = Position(110, 70, None, None, 70, None, 120, None, None)
laughingPosition1 = Position(None, None, None, None, None, 90, 130, None, None)
laughingPosition2 = Position(None, None, None, None, None, 70, 115, None, None)
noddingYes1 = Position(None, None, None, None, None, None, 80, None, None)
noddingYes2 = Position(None, None, None, None, None, None, 130, None, None)
shakingNo1 = Position(None, None, None, None, None, None, None, 110, None)
shakingNo2 = Position(None, None, None, None, None, None, None, 80, None)