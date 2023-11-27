package ordina.youbionic.service;

import ordina.youbionic.configuration.ServoEnum;

// This class has the sole function to keep track of current servomotor angles,
// and whether the servomotor is currently moving.
// We use it to determine the speed of certain slower movements.
public class ServoTracker {
    int eyeLeft_pos;
    boolean eyeLeft_inMotion;
    int eyeRight_pos;
    boolean eyeRight_inMotion;
    int eyeLeftOpen_pos;
    boolean eyeLeftOpen_inMotion;
    int eyeRightOpen_pos;
    boolean eyeRightOpen_inMotion;
    int eyesUpDown_pos;
    boolean eyesUpDown_inMotion;
    int mouth_pos;
    boolean mouth_inMotion;
    int headTilt_pos;
    boolean headTilt_inMotion;
    int headPivot_pos;
    boolean headPivot_inMotion;
    int headSwivel_pos;
    boolean headSwivel_inMotion;

    public ServoTracker() {
        this.eyeLeft_inMotion = false;
        this.eyeRight_inMotion = false;
        this.eyeLeftOpen_inMotion = false;
        this.eyeRightOpen_inMotion = false;
        this.eyesUpDown_inMotion = false;
        this.mouth_inMotion = false;
        this.headTilt_inMotion = false;
        this.headPivot_inMotion = false;
        this.headSwivel_inMotion = false;
    }

    public int getCurrentRotation(ServoEnum servo){
        return switch (servo) {
            case EYE_LEFT -> eyeLeft_pos;
            case EYE_RIGHT -> eyeRight_pos;
            case EYE_LEFT_OPEN -> eyeLeftOpen_pos;
            case EYE_RIGHT_OPEN -> eyeRightOpen_pos;
            case EYES_UP_DOWN -> eyesUpDown_pos;
            case MOUTH -> mouth_pos;
            case HEAD_TILT -> headTilt_pos;
            case HEAD_PIVOT -> headPivot_pos;
            case HEAD_SWIVEL -> headSwivel_pos;
        };
    }

    public void setCurrentRotation(ServoEnum servo, int angle){
        switch(servo){
            case EYE_LEFT -> this.eyeLeft_pos = angle;
            case EYE_RIGHT -> this.eyeRight_pos = angle;
            case EYE_LEFT_OPEN -> this.eyeLeftOpen_pos = angle;
            case EYE_RIGHT_OPEN -> this.eyeRightOpen_pos = angle;
            case EYES_UP_DOWN -> this.eyesUpDown_pos = angle;
            case MOUTH -> this.mouth_pos = angle;
            case HEAD_TILT -> this.headTilt_pos = angle;
            case HEAD_SWIVEL -> this.headSwivel_pos = angle;
            case HEAD_PIVOT -> this.headPivot_pos = angle;
        }
    }

    public void setIsMoving(ServoEnum servo, boolean isMoving){
        switch(servo){
            case EYE_LEFT -> this.eyeLeft_inMotion = isMoving;
            case EYE_RIGHT -> this.eyeRight_inMotion = isMoving;
            case EYE_LEFT_OPEN -> this.eyeLeftOpen_inMotion = isMoving;
            case EYE_RIGHT_OPEN -> this.eyeRightOpen_inMotion = isMoving;
            case EYES_UP_DOWN -> this.eyesUpDown_inMotion = isMoving;
            case MOUTH -> this.mouth_inMotion = isMoving;
            case HEAD_TILT -> this.headTilt_inMotion = isMoving;
            case HEAD_SWIVEL -> this.headSwivel_inMotion = isMoving;
            case HEAD_PIVOT -> this.headPivot_inMotion = isMoving;
        }
    }

    public boolean getIsMoving(ServoEnum servo){
        return switch (servo) {
            case EYE_LEFT -> eyeLeft_inMotion;
            case EYE_RIGHT -> eyeRight_inMotion;
            case EYE_LEFT_OPEN -> eyeLeftOpen_inMotion;
            case EYE_RIGHT_OPEN -> eyeRightOpen_inMotion;
            case EYES_UP_DOWN -> eyesUpDown_inMotion;
            case MOUTH -> mouth_inMotion;
            case HEAD_TILT -> headTilt_inMotion;
            case HEAD_PIVOT -> headPivot_inMotion;
            case HEAD_SWIVEL -> headSwivel_inMotion;
        };
    }

}
