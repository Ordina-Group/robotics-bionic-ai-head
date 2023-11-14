package ordina.youbionic.service;

import ordina.youbionic.Exception.IllegalEnumValueException;
import ordina.youbionic.Exception.InvalidCommandException;
import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import org.springframework.stereotype.Service;

@Service
public class ServoService {
    private final RabbitMQPublisher publisher;

    public ServoService(){
        try {
            this.publisher = new RabbitMQPublisher();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    public String test0() throws Exception{
        String message = "15,0,0";
        try {
            publish(message);
        } catch (InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
        return "Great success";
    }

    //TODO: DEZE SCHRIJVEN!

    public String testAll() throws Exception{
        String[] messages = {"0,0,1", "1,0,1", "2,0,1", "3,0,1", "4,0,1", "5,0,1", "13,0,1", "14,0,1", "15,0,1"};
        for(String message : messages){
            publish(message);

        }
        return "All servomotors should move. If not, one might have broken.";
    }

    // This method resets all servomotors to 90 degrees. This is the angle we used during assembly, and should be the neutral resting position for the head.
    public String reset() throws Exception{
        String[] messages = {"0,90,1", "1,90,1", "2,90,1", "3,90,1", "4,90,1", "5,90,1", "13,90,1", "14,90,1", "15,90,1"};
        for(String message : messages){
            publish(message);
        }
        return "All servomotors reset to 90 degrees and ready for assembly!";
    }

    //TODO: DEZE AFMAKEN!!
    public String manualServoRotation(String message) throws Exception{
        try{
            publish(message);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        String[] splitMessage = message.split(",");
        return "Successfully moved servomotor number " + splitMessage[0] + " by " + splitMessage[1] + " degrees.";
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

    private void publish(String message) throws InvalidCommandException, IllegalEnumValueException {
        validateCommand(message);
        publisher.publish(QueueEnum.SERVO, message);
    }

}
