package ordina.youbionic.service;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.exception.IllegalEnumValueException;
import ordina.youbionic.exception.InvalidCommandException;
import ordina.youbionic.configuration.ServoEnum;
import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import org.springframework.stereotype.Service;
import ordina.youbionic.configuration.ServoConfig;

import java.util.*;

@Service
//@RequiredArgsConstructor
public class ServoService {
    private final RabbitMQPublisher publisher;
    private final ServoConfig config;
    private final ServoTracker tracker;

    public ServoService(){
        this.config = new ServoConfig();
        try {
            this.publisher = new RabbitMQPublisher();
            this.tracker = new ServoTracker();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void closeEyes() throws Exception{
        final boolean override = true;
        try{
            publish(ServoEnum.EYE_RIGHT_OPEN, config.getMaxRotation(ServoEnum.EYE_RIGHT_OPEN), override);
            publish(ServoEnum.EYE_LEFT_OPEN, config.getMinRotation(ServoEnum.EYE_LEFT_OPEN), override);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void openEyes() throws Exception{
        final boolean override = true;
        try{
            publish(ServoEnum.EYE_RIGHT_OPEN, config.getDefaultRotation(ServoEnum.EYE_RIGHT_OPEN), override);
            publish(ServoEnum.EYE_LEFT_OPEN, config.getDefaultRotation(ServoEnum.EYE_LEFT_OPEN), override);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void blink() throws Exception{
        // TODO: Overal waar 'Thread.sleep' staat, dat vervangen met non-blocking sleep
        // TODO: virtual threads?
        try{
            closeEyes();
            Thread.sleep(250);
            openEyes();
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void laugh() throws Exception{
        final boolean override = true;
        final Map<ServoEnum, Integer> basePosition = Map.of(ServoEnum.HEAD_TILT, 110, ServoEnum.EYE_RIGHT_OPEN, 80, ServoEnum.EYE_LEFT_OPEN, 100, ServoEnum.EYES_UP_DOWN, 90, ServoEnum.EYE_LEFT, 90, ServoEnum.MOUTH, 60, ServoEnum.HEAD_SWIVEL, 95);
        final Map<ServoEnum, Integer> eyeRoll = Map.of(ServoEnum.EYE_LEFT, 110, ServoEnum.EYES_UP_DOWN, 70, ServoEnum.HEAD_TILT,120);
        final Map<ServoEnum, Integer> laughPos1 = Map.of(ServoEnum.MOUTH, 90, ServoEnum.HEAD_TILT, 130);
        final Map<ServoEnum, Integer> laughPos2 = Map.of(ServoEnum.MOUTH, 70, ServoEnum.HEAD_TILT, 115);
        try{
            batchPublish(basePosition, override);
            Thread.sleep(100);
            batchPublish(eyeRoll, override);
            Thread.sleep(200);
            closeEyes();
            for(int i = 0; i < 8; i++){
                batchPublish(laughPos1, override);
                Thread.sleep(200);
                batchPublish(laughPos2, override);
                Thread.sleep(200);
            }
            batchPublish(basePosition, override);
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void nodYes() throws Exception{
        try{
            closeEyes();
            final boolean override = true;
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
            final boolean override = true;
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
        final boolean override = true;
        Map<ServoEnum, Integer> map = new HashMap<>();
        for(ServoEnum servo : ServoEnum.values()){
            map.put(servo, 90);
        }
        batchPublish(map, override);
    }

    public void rest() throws Exception{
        final boolean override = true;
        Map<ServoEnum, Integer> map = new HashMap<>();
        for(ServoEnum servo : ServoEnum.values()){
            map.put(servo, config.getDefaultRotation(servo));
        }
        batchPublish(map, override);
    }

    public String configure(final int servo) throws Exception{
        try{
            final ServoEnum servoEnum = config.getServoEnum(servo);
            publish(servoEnum, 80, true);
            Thread.sleep(1000);
            publish(servoEnum, 100, true);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        return "Successfully moved servomotor number " + servo;
    }

    public String manual(final int servo, final int angle) throws Exception{
        try{
            final ServoEnum servoEnum = config.getServoEnum(servo);
            publish(servoEnum, angle, true);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        return "Successfully moved servomotor number " + servo + " to " + angle + " degrees.";
    }

    // In this method, we validate if the message we're about to publish to RabbitMQ meets all requirements. For the YouBionic head, we have exactly 9 servomotors, they are plugged in on pins 0,1,2,3,4,5, 13,14,15
    // They can rotate between 0 and 180 degrees. The messages must also contain an override value of 0 or 1. Nothing else can be included.
    private String validateCommand(final String message) throws InvalidCommandException {
        // Check if the command is empty
        if(message == null  || message.isEmpty()){
            throw new InvalidCommandException("Command is empty.");
        }
        final String[] splitMessage = message.split(",");

        // Create a validated command we can use later
        StringBuilder validatedCommand = new StringBuilder();

        // Check if command has appropriate amount of elements
        final int amountOfInstructions = Integer.parseInt(splitMessage[0]);
        if(amountOfInstructions == 0){
            throw new InvalidCommandException("Command is faulty. It has declared to have 0 elements.");
        }
        if(splitMessage.length != (amountOfInstructions * 2) + 2){
            throw new InvalidCommandException("Command is faulty. It has " + splitMessage.length + " elements. It needs 1 for the length of the command, 2 for every movable servomotor, and 1 last one for the override. ");
        }
        validatedCommand.append(amountOfInstructions).append(",");

        // Check if override is correct
        final int override = Integer.parseInt(splitMessage[splitMessage.length - 1]);
        if (override < 0 || override > 1) {
            throw new InvalidCommandException("Command is faulty. Override should be 0 or 1, not " + override + ".");
        }

        // Copy command without amount of instructions and override, so we can easily iterate over it
        int[] numbers = new int[splitMessage.length - 2];
        for(int i = 0, k = 0; i < splitMessage.length; i++){
            if(i != 0 && i != splitMessage.length - 1){
                numbers[k] = Integer.parseInt(splitMessage[i]);
                k++;
            }
        }

        // Iterate over the separate commands, to see if they are correct
        for(int i = 0; i < numbers.length;) {
            final int servoNumber = numbers[i];
            if (servoNumber < 0 || servoNumber > 15) {
                throw new InvalidCommandException("Servomotor out of bounds. Tried to send message to servomotor number " + numbers[0] + ".");
            }
            validatedCommand.append(numbers[i]).append(",");
            i++;
            final int angle = numbers[i];
            if (angle < 0 || angle > 180) {
                throw new InvalidCommandException("Angle out of bounds. Tried to move servomotor by " + splitMessage[1] + " degrees. Range is 0-180 degrees.");
            }
            validatedCommand.append(numbers[i]).append(",");
            i++;
        }

        validatedCommand.append(override);
        return validatedCommand.toString();
    }

    // This method is (not yet) used to change the desired command to be within bounds
    public String placeWithinBounds(final String command) throws Exception {
        final String[] splitMessage = command.split(",");
        if(splitMessage.length != 3){
            return command;
        }
        ServoEnum servo = config.getServoEnum(Integer.parseInt(splitMessage[0]));
        final int desiredAngle = Integer.parseInt(splitMessage[1]);
        if(desiredAngle < config.getMinRotation(servo)){
            return splitMessage[0] + config.getMinRotation(servo) + splitMessage[2];
        }
        else if(desiredAngle > config.getMaxRotation(servo)){
            return splitMessage[0] + config.getMaxRotation(servo) + splitMessage[2];
        }
        return command;
    }

    private void publish(final ServoEnum servoEnum, final int angle, final boolean override) throws InvalidCommandException, IllegalEnumValueException {
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
        final String command = "1," + config.getServoNumber(servoEnum) + "," + angle + "," + overwrite;
        publisher.publish(QueueEnum.SERVO, validateCommand(command));
        tracker.setCurrentRotation(servoEnum, angle);
    }

    public void testSlowlyMove() throws InvalidCommandException, InterruptedException, IllegalEnumValueException {
        slowlyMove(ServoEnum.HEAD_SWIVEL, 50, false, 3, 100);
        slowlyMove(ServoEnum.HEAD_SWIVEL, 130, false, 3, 100);
    }

    private void slowlyMove(final ServoEnum servoEnum, final int desiredAngle, final boolean override, final int incrementInDegrees, final int stepsInMilliseconds) throws InvalidCommandException, IllegalEnumValueException, InterruptedException {
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

    private void batchPublish(final Map<ServoEnum, Integer> positions, final boolean override) throws InvalidCommandException, IllegalEnumValueException {
        StringBuilder cmd = new StringBuilder();
        int amountOfCommands = positions.size();
        cmd.append(amountOfCommands);
        for(Map.Entry<ServoEnum, Integer> entry : positions.entrySet()){
            if(!override) {
                if (tracker.getIsMoving(entry.getKey())) {
                    return;
                }
            }
            cmd.append(entry.getKey()).append(",").append(entry.getValue()).append(",");
        }
        cmd.append(override);
        publisher.publish(QueueEnum.SERVO, validateCommand(cmd.toString()));
        for(Map.Entry<ServoEnum, Integer> entry : positions.entrySet()){
            tracker.setCurrentRotation(entry.getKey(), entry.getValue());
        }
    }

}
