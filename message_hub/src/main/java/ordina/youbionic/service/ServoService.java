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
        String message = "15,90,0";
        try {
            publish(message);
        } catch (InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
        return "Great success";
    }

    public void closeEyes() throws Exception{
        String closeRight = "3,80,1";
        String closeLeft = "2,120,1";
        try{
            publish(closeLeft);
            publish(closeRight);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void openEyes() throws Exception{
        String openRight = "3,120,1";
        String openLeft = "2,80,1";
        try{
            publish(openLeft);
            publish(openRight);
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void blink() throws Exception{
        try{
            closeEyes();
            Thread.sleep(100);
            openEyes();
        } catch(InvalidCommandException e) {
            throw new InvalidCommandException(e.getMessage());
        }
    }
    public String laugh() throws Exception{
        String[] baseposition = {"13,110,1", "2,80,1", "3,100,1", "4,90,1", "1,90,1", "5,60,1", "14,95,1"};
        String[] eyeroll = {"1,110,1", "4,70,1", "13,120,1"};
        String[] laugh1 = {"5,90,1", "13,130,1"};
        String[] laugh2 = {"5,70,1", "13,115,1"};
        try{
            for(String msg : baseposition){
                publish(msg);
            }
            Thread.sleep(100);
            for(String msg : eyeroll){
                publish(msg);
            }
            Thread.sleep(200);
            closeEyes();
            for(int i = 0; i < 8; i++){
                for(String message : laugh1){
                    publish(message);
                }
                Thread.sleep(200);
                for(String message : laugh2){
                    publish(message);
                }
                Thread.sleep(200);
            }
            for(String msg : baseposition){
                publish(msg);
            }
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
        return "Hahaha";
    }

    public void nodYes() throws Exception{
        try{
            closeEyes();
            String down = "13,80,1";
            String up = "13,130,1";
            String normal = "13,110,1";
            for(int i = 0; i < 3; i++){
                publish(down);
                Thread.sleep(400);
                publish(up);
                Thread.sleep(400);
            }
            publish(normal);
            openEyes();
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }

    public void shakeNo() throws Exception{
        try{
            closeEyes();
            String left = "14,105,1";
            String right = "14,85,1";
            String normal = "14,95,1";
            for(int i = 0; i < 3; i++){
                publish(left);
                Thread.sleep(500);
                publish(right);
                Thread.sleep(500);
            }
            publish(normal);
            openEyes();
        } catch(InvalidCommandException e){
            throw new InvalidCommandException(e.getMessage());
        }
    }
    public String testAll() throws Exception{
        String[] messages = {"0,60,1", "1,60,1", "2,60,1", "3,60,1", "4,60,1", "5,60,1", "13,60,1", "14,60,1", "15,60,1"};
        String[] messages2 = {"0,120,1", "1,120,1", "2,120,1", "3,120,1", "4,120,1", "5,120,1", "13,120,1", "14,120,1", "15,120,1"};
        for(String message : messages){
            publish(message);
            Thread.sleep(500);
        }
        Thread.sleep(2000);
        for(String message : messages2){
            publish(message);
            Thread.sleep(500);
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

    public String rest() throws Exception{
        String[] messages = {"0,90,1", "1,100,1", "2,80,1", "3,80,1", "4,105,1", "5,70,1", "13,110,1", "14,95,1", "15,95,1"};
        for(String message : messages){
            publish(message);
        }
        return "Head set in neutral position!";
    }

    public String config(String servo) throws Exception{
        try{
            String message = servo + ",80,1";
            publish(message);
            Thread.sleep(1000);
            String message2 = servo + ",100,1";
            publish(message2);
        } catch (InvalidCommandException e) {
            throw new RuntimeException(e);
        }
        return "Successfully moved servomotor number " + servo;
    }

    public String manual(String servo, String angle) throws Exception{
        try{
            String message = servo + "," + angle + ",1";
            publish(message);
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

    private void publish(String message) throws InvalidCommandException, IllegalEnumValueException {
        validateCommand(message);
        publisher.publish(QueueEnum.SERVO, message);
    }

}
