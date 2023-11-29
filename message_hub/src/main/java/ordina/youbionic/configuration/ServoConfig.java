package ordina.youbionic.configuration;

import ordina.youbionic.exception.IllegalEnumValueException;


// In this config class, we define what servomotor is hooked up to what pins on the Adafruit PCA9685.
// In order to find out what is plugged in where, use the 'config' endpoint and try out pins 0-15.
// Then update the strings for the pinNumbers below as suited.
// Also customisable is the minimum, maximum and default rotation values for each servomotor.
// We can set these to avoid accidentally going out of bounds or breaking the plastic,
// And so we can reset the head to a neutral resting position.
public class ServoConfig {
    private static class eyeLeft {
        static final int pinNumber() {return 0;}
        static final int defaultRotation() {
            return 100;
        }
        static final int minRotation(){
            return 80;
        }
        static final int maxRotation(){
            return 115;
        }
    }
    private static class eyeRight{
        static final int pinNumber() {
            return 1;
        }
        static final int  defaultRotation() {
            return 100;
        }
        static final int minRotation(){
            return 80;
        }
        static final int maxRotation(){
            return 115;
        }
    }
    private static class eyeLeftOpen {
        static int pinNumber() {
            return 3;
        }
        static final int defaultRotation() {
            return 100;
        }
        final static int minRotation(){
            return 80;
        }
        final static int maxRotation(){return 120;}
    }
    private static class eyeRightOpen{
        static final int pinNumber() {
            return 2;
        }
        static final int defaultRotation() {return 80;}
        static final int minRotation(){
            return 80;
        }
        static final int maxRotation(){
            return 120;
        }
    }
    private static class eyesUpDown {
        // Makes both eyes look up or down simultaneously.
        static final int pinNumber() {
            return 4;
        }
        static final int defaultRotation() {
            return 105;
        }
        static final int minRotation(){
            return 70;
        }
        static final int maxRotation(){
            return 180;
        }
    }
    private static class mouth{
        // Opens the mouth.
        static final int pinNumber() {
            return 5;
        }
        static final int defaultRotation() { return 70; }

        // The min/max rotation values for the mouth are dependent on the headTilt.
        // TODO: FIGURE OUT A WAY TO MAKE THE MOUTH OPEN/CLOSE DEPEND ON HEADTILT
        static final int minRotation(){
            return 60;
        }
        static final int maxRotation(){ return 100; }
    }
    private static class headTilt{
        // Makes the head look up or down.
        static final int pinNumber() {
            return 13;
        }
        static final int defaultRotation() { return 110; }
        static final int minRotation(){
            return 70;
        }
        static final int maxRotation(){
                return 150;
        }
    }
    private static class headSwivel{
        // Makes the head look left and right.
        static final int pinNumber() {
            return 14;
        }
        static final int defaultRotation() {
            return 95;
        }
        static final int minRotation(){
            return 50;
        }
        static final int maxRotation(){
            return 130;
        }
    }
    private static class headPivot{
        // Rotates the neck left and right, which moves the head horizontally.
        static final int pinNumber() {
            return 15;
        }
        static final int defaultRotation() {   return 95; }
        static final int minRotation(){ return 70; }
        static final int maxRotation(){ return 110; }
    }


    // Config ends here; from here on it is methods to get the right values.

    public int getServoNumber(ServoEnum servo) throws IllegalEnumValueException {
        return switch (servo) {
            case EYE_LEFT -> eyeLeft.pinNumber();
            case EYE_RIGHT -> eyeRight.pinNumber();
            case EYE_LEFT_OPEN -> eyeLeftOpen.pinNumber();
            case EYE_RIGHT_OPEN -> eyeRightOpen.pinNumber();
            case EYES_UP_DOWN -> eyesUpDown.pinNumber();
            case MOUTH -> mouth.pinNumber();
            case HEAD_TILT -> headTilt.pinNumber();
            case HEAD_SWIVEL -> headSwivel.pinNumber();
            case HEAD_PIVOT -> headPivot.pinNumber();
            default ->
                    throw new IllegalEnumValueException("Attempted to get servomotor number for a servomotor that doesn't exist");
        };
    }

    public int getMinRotation(ServoEnum servo) throws IllegalEnumValueException{
        return switch (servo) {
            case EYE_LEFT -> eyeLeft.minRotation();
            case EYE_RIGHT -> eyeRight.minRotation();
            case EYE_LEFT_OPEN -> eyeLeftOpen.minRotation();
            case EYE_RIGHT_OPEN -> eyeRightOpen.minRotation();
            case EYES_UP_DOWN -> eyesUpDown.minRotation();
            case MOUTH -> mouth.minRotation();
            case HEAD_TILT -> headTilt.minRotation();
            case HEAD_SWIVEL -> headSwivel.minRotation();
            case HEAD_PIVOT -> headPivot.minRotation();
            default ->
                    throw new IllegalEnumValueException("Attempted to get servomotor number for a servomotor that doesn't exist");
        };
    }

    public int getMaxRotation(ServoEnum servo) throws IllegalEnumValueException{
        return switch (servo) {
            case EYE_LEFT -> eyeLeft.maxRotation();
            case EYE_RIGHT -> eyeRight.maxRotation();
            case EYE_LEFT_OPEN -> eyeLeftOpen.maxRotation();
            case EYE_RIGHT_OPEN -> eyeRightOpen.maxRotation();
            case EYES_UP_DOWN -> eyesUpDown.maxRotation();
            case MOUTH -> mouth.maxRotation();
            case HEAD_TILT -> headTilt.maxRotation();
            case HEAD_SWIVEL -> headSwivel.maxRotation();
            case HEAD_PIVOT -> headPivot.maxRotation();
            default ->
                    throw new IllegalEnumValueException("Attempted to get servomotor number for a servomotor that doesn't exist");
        };
    }

    public int getDefaultRotation(ServoEnum servo) throws IllegalEnumValueException{
        return switch (servo) {
            case EYE_LEFT -> eyeLeft.defaultRotation();
            case EYE_RIGHT -> eyeRight.defaultRotation();
            case EYE_LEFT_OPEN -> eyeLeftOpen.defaultRotation();
            case EYE_RIGHT_OPEN -> eyeRightOpen.defaultRotation();
            case EYES_UP_DOWN -> eyesUpDown.defaultRotation();
            case MOUTH -> mouth.defaultRotation();
            case HEAD_TILT -> headTilt.defaultRotation();
            case HEAD_SWIVEL -> headSwivel.defaultRotation();
            case HEAD_PIVOT -> headPivot.defaultRotation();
            default ->
                    throw new IllegalEnumValueException("Attempted to get servomotor number for a servomotor that doesn't exist");
        };
    }

    public ServoEnum getServoEnum(int number) throws Exception {
        if(eyeLeft.pinNumber() == number){
            return ServoEnum.EYE_LEFT;
        }
        if(eyeRight.pinNumber() == number){
            return ServoEnum.EYE_RIGHT;
        }
        if(eyeLeftOpen.pinNumber() == number){
            return ServoEnum.EYE_LEFT_OPEN;
        }
        if(eyeRightOpen.pinNumber() == number){
            return ServoEnum.EYE_RIGHT_OPEN;
        }
        if(eyesUpDown.pinNumber() == number){
            return ServoEnum.EYES_UP_DOWN;
        }
        if(mouth.pinNumber() == number){
            return ServoEnum.MOUTH;
        }
        if(headPivot.pinNumber() == number){
            return ServoEnum.HEAD_PIVOT;
        }
        if(headSwivel.pinNumber() == number){
            return ServoEnum.HEAD_SWIVEL;
        }
        if(headTilt.pinNumber() == number){
            return ServoEnum.HEAD_TILT;
        }
        else{
            throw new Exception("Servomotor doesn't exist");
        }
    }
}
