package ordina.youbionic.service;

import ordina.youbionic.Exception.IllegalEnumValueException;
import ordina.youbionic.Exception.InvalidCommandException;
import ordina.youbionic.configuration.ServoEnum;
import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import org.springframework.stereotype.Service;
import ordina.youbionic.configuration.ServoConfig;

import java.util.*;

@Service
public class ServoService {
    private final RabbitMQPublisher publisher;
    private final ServoConfig config;
    private final ServoTracker tracker;


    public ServoService(){
        this.config = new ServoConfig();
        try {
            this.publisher = new RabbitMQPublisher();
            this.tracker = new ServoTracker();
            publisher.purge(QueueEnum.SERVO);
            rest();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void closeEyes() throws Exception{
        boolean override = true;
        try{
            publish(ServoEnum.EYE_RIGHT_OPEN, 80, override);
            publish(ServoEnum.EYE_LEFT_OPEN, 120, override);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void openEyes() throws Exception{
        boolean override = true;
        try{
            publish(ServoEnum.EYE_RIGHT_OPEN, 120, override);
            publish(ServoEnum.EYE_LEFT_OPEN, 80, override);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void blink() throws Exception{
        // TODO: Overal waar 'Thread.sleep' staat, dat vervangen met non-blocking sleep
        // TODO: virtual threads?
        try{
            closeEyes();
            Thread.sleep(100);
            openEyes();
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }
    // TODO: DEZE FIXEN!
    public void laugh() throws Exception{
        boolean override = true;
        Map<ServoEnum, Integer> basePosition = Map.of(ServoEnum.HEAD_TILT, 110, ServoEnum.EYE_RIGHT_OPEN, 80, ServoEnum.EYE_LEFT_OPEN, 100, ServoEnum.EYES_UP_DOWN, 90, ServoEnum.EYE_LEFT, 90, ServoEnum.MOUTH, 60, ServoEnum.HEAD_SWIVEL, 95);
        Map<ServoEnum, Integer> eyeRoll = Map.of(ServoEnum.EYE_LEFT, 110, ServoEnum.EYES_UP_DOWN, 70, ServoEnum.HEAD_TILT,120);
        Map<ServoEnum, Integer> laughPos1 = Map.of(ServoEnum.MOUTH, 90, ServoEnum.HEAD_TILT, 130);
        Map<ServoEnum, Integer> laughPos2 = Map.of(ServoEnum.MOUTH, 70, ServoEnum.HEAD_TILT, 115);
        try{
            for(Map.Entry<ServoEnum, Integer> entry : basePosition.entrySet()){
                publish(entry.getKey(), entry.getValue(), override);
            }
            Thread.sleep(100);
            for(Map.Entry<ServoEnum, Integer> entry : eyeRoll.entrySet()){
                publish(entry.getKey(), entry.getValue(), override);
            }
            Thread.sleep(200);
            closeEyes();
            for(int i = 0; i < 8; i++){
                for(Map.Entry<ServoEnum, Integer> entry : laughPos1.entrySet()){
                    publish(entry.getKey(), entry.getValue(), override);
                }
                Thread.sleep(200);
                for(Map.Entry<ServoEnum, Integer> entry : laughPos2.entrySet()){
                    publish(entry.getKey(), entry.getValue(), override);
                }
                Thread.sleep(200);
            }
            for(Map.Entry<ServoEnum, Integer> entry : basePosition.entrySet()){
                publish(entry.getKey(), entry.getValue(), override);
            }
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void nodYes() throws Exception{
        try{
            closeEyes();
            boolean override = true;
            for(int i = 0; i < 3; i++){
                publish(ServoEnum.HEAD_TILT, 80, override);
                Thread.sleep(400);
                publish(ServoEnum.HEAD_TILT, 130, override);
                Thread.sleep(400);
            }
            publish(ServoEnum.HEAD_TILT, 110, override);
            openEyes();
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void shakeNo() throws Exception{
        try{
            closeEyes();
            boolean override = true;
            for(int i = 0; i < 3; i++){
                publish(ServoEnum.HEAD_SWIVEL, 105, override);
                Thread.sleep(500);
                publish(ServoEnum.HEAD_SWIVEL, 85, override);
                Thread.sleep(500);
            }
            publish(ServoEnum.HEAD_SWIVEL, 95, override);
            openEyes();
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }

    // This method resets all servomotors to 90 degrees. This is the angle we used during assembly, and should be the neutral resting position for the head.
    public void reset() throws Exception{
        boolean override = true;
        for(ServoEnum servo : ServoEnum.values()){
            publish(servo, 90, override);
        }
    }

    public void rest() throws Exception{
        boolean override = true;
        for(ServoEnum servo : ServoEnum.values()){
            int angle = config.getDefaultRotation(servo);
            publish(servo, angle, override);
        }
    }

    public String configure(int servo) throws Exception{
        try{
            ServoEnum servoEnum = config.getServoEnum(servo);
            publish(servoEnum, 80, true);
            Thread.sleep(1000);
            publish(servoEnum, 100, true);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        return "Successfully moved servomotor number " + servo;
    }

    public String manual(int servo, int angle) throws Exception{
        try{
            ServoEnum servoEnum = config.getServoEnum(servo);
            publish(servoEnum, angle, true);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        return "Successfully moved servomotor number " + servo + " to " + angle + " degrees.";
    }

    // In this method, we validate if the message we're about to publish to RabbitMQ meets all requirements. For the YouBionic head, we have exactly 9 servomotors, they are plugged in on pins 0,1,2,3,4,5, 13,14,15
    // They can rotate between 0 and 180 degrees. The messages must also contain an override value of 0 or 1. Nothing else can be included.
    private void validateCommand(String message) throws InvalidCommandException {
        if(message == null  || message.isEmpty()){
            throw new InvalidCommandException("Command is empty.");
        }
        String[] splitMessage = message.split(",");
        if(splitMessage.length != 3){
            throw new InvalidCommandException("Command is faulty. It has " + splitMessage.length + " elements, while it needs exactly 3.");
        }
        try{
            int servoNumber = Integer.parseInt(splitMessage[0]);
            if(servoNumber < 0 || servoNumber > 15){
                throw new InvalidCommandException("Servomotor out of bounds. Tried to send message to servomotor number " + splitMessage[0] + ".");
            }
        } catch (NumberFormatException e){
            throw new InvalidCommandException("Command is faulty. Tried to send message to servomotor number " + splitMessage[0] + ".");
        }
        try{
            int angle = Integer.parseInt(splitMessage[1]);
            if(angle < 0 || angle > 180){
                throw new InvalidCommandException("Angle out of bounds. Tried to move servomotor by " + splitMessage[1] + " degrees. Range is 0-180 degrees.");
            }
        } catch (NumberFormatException e){
            throw new InvalidCommandException("Command is faulty. Tried to move servomotor by " + splitMessage[1] + " degrees.");
        }
        try{
            int override = Integer.parseInt(splitMessage[2]);
            if(override < 0 || override > 1){
                throw new InvalidCommandException("Command is faulty. Override should be 0 or 1, not " + splitMessage[2] + ".");
            }
        } catch (NumberFormatException e){
            throw new InvalidCommandException("Command is faulty. Override should be 0 or 1, not " + splitMessage[2] + ".");
        }
    }

    // This method is used to change the desired command to be within bounds
    public String placeWithinBounds(String command) throws Exception {
        String[] splitMessage = command.split(",");
        if(splitMessage.length != 3){
            return command;
        }
        ServoEnum servo = config.getServoEnum(Integer.parseInt(splitMessage[0]));
        int desiredAngle = Integer.parseInt(splitMessage[1]);
        if(desiredAngle < config.getMinRotation(servo)){
            return splitMessage[0] + config.getMinRotation(servo) + splitMessage[2];
        }
        else if(desiredAngle > config.getMaxRotation(servo)){
            return splitMessage[0] + config.getMaxRotation(servo) + splitMessage[2];
        }
        return command;
    }

    private void publish(ServoEnum servoEnum, int angle, boolean override) throws InvalidCommandException, IllegalEnumValueException {
        if(tracker.getIsMoving(servoEnum)){
            if(!override){
                return;
            }
        }
        int overwrite;
        if(override){
            overwrite = 1;
        }
        else{
            overwrite = 0;
        }
        String command = config.getServoNumber(servoEnum) + "," + angle + "," + overwrite;
        validateCommand(command);
        publisher.publish(QueueEnum.SERVO, command);
        tracker.setCurrentRotation(servoEnum, angle);
    }

    private void slowlyMove(ServoEnum servoEnum, int desiredAngle, boolean override, int incrementInDegrees, int stepsInMilliseconds) throws InvalidCommandException, IllegalEnumValueException, InterruptedException {
        if(incrementInDegrees < 0){
            throw new InvalidCommandException("Tried to move the servomotor number " + config.getServoNumber(servoEnum) + " by " + incrementInDegrees + " degrees. It can't be negative");
        }
        if(stepsInMilliseconds < 0){
            throw new InvalidCommandException("Tried to move a servomotor every negative amount of milliseconds (" + incrementInDegrees + " degrees every " + stepsInMilliseconds + "ms)");
        }
        if(tracker.getIsMoving(servoEnum)){
            if(!override){
                return;
            }
        }
        int currentAngle = tracker.getCurrentRotation(servoEnum);
        tracker.setIsMoving(servoEnum, true);
        while(currentAngle != desiredAngle){
          if(currentAngle < desiredAngle && currentAngle + incrementInDegrees <= desiredAngle){
              publish(servoEnum, currentAngle + incrementInDegrees, override);
              currentAngle = currentAngle + incrementInDegrees;
              Thread.sleep(stepsInMilliseconds);
          }
          else if(currentAngle < desiredAngle && currentAngle + incrementInDegrees > desiredAngle){
              currentAngle = desiredAngle;
              publish(servoEnum, desiredAngle, override);
          }
          else if(currentAngle > desiredAngle && currentAngle - incrementInDegrees >= desiredAngle){
              publish(servoEnum, currentAngle - incrementInDegrees, override);
              currentAngle = currentAngle - incrementInDegrees;
              Thread.sleep(stepsInMilliseconds);
          }
          else if(currentAngle > desiredAngle && currentAngle - incrementInDegrees < desiredAngle){
              publish(servoEnum, desiredAngle, override);
              currentAngle = desiredAngle;
          }
        }
        tracker.setIsMoving(servoEnum, false);
    }

}
