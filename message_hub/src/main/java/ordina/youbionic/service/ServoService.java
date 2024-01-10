package ordina.youbionic.service;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.exception.IllegalEnumValueException;
import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ServoService {
    private final RabbitMQPublisher publisher;
//    private final ServoTracker tracker;

    public ServoService(){
        try {
            this.publisher = new RabbitMQPublisher();
//            this.tracker = new ServoTracker();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void closeEyes() throws Exception{
        publish("close_eyes");
    }

    public void openEyes() throws Exception{
        publish("open_eyes");
    }

    public void blink() throws Exception{
        publish("blink");
    }

    public void laugh() throws Exception{
        publish("laugh");
    }

    public void nodYes() throws Exception{
        publish("nod_yes");
    }

    public void shakeNo() throws Exception{
        publish("shake_no");
    }

    // This method resets all servomotors to 90 degrees. This is the angle we used during assembly, and should be the neutral resting position for the head.
    public void reset() throws Exception{
        publish("all90");
    }

    public void rest() throws Exception{
        publish("rest");
    }

    public String configure(final int servo) throws Exception{
        publish("config:" + servo);
        return "Moved servo number: " + servo + ". If nothing moved, something is broken.";
    }

    public String manualWithNumber(final int servo, final int angle) throws Exception{
        publish("manualWithNumber:" + servo + ":" + angle);
        return "Successfully moved servomotor number " + servo + " to " + angle + " degrees.";
    }

    public String manualWithName(final String servo, final int angle) throws Exception{
        publish("manualWithName:" + servo + ":" + angle);
        return "Successfully moved servomotor with name " + servo + " to " + angle + " degrees.";
    }

    private void publish(final String message) throws IllegalEnumValueException {
        publisher.publish(QueueEnum.SERVO, message);
    }


//    private void slowlyMove(final ServoEnum servoEnum, final int desiredAngle, final boolean override, final int incrementInDegrees, final int stepsInMilliseconds) throws InvalidCommandException, IllegalEnumValueException, InterruptedException {
//        if(incrementInDegrees < 0){
//            throw new InvalidCommandException("Tried to move the servomotor number " + config.getServoNumber(servoEnum) + " by " + incrementInDegrees + " degrees. It can't be negative");
//        }
//        if(stepsInMilliseconds < 0){
//            throw new InvalidCommandException("Tried to move a servomotor every negative amount of milliseconds (" + incrementInDegrees + " degrees every " + stepsInMilliseconds + "ms)");
//        }
//        if(tracker.getIsMoving(servoEnum)){
//            if(!override){
//                return;
//            }
//        }
//        int currentAngle = tracker.getCurrentRotation(servoEnum);
//        tracker.setIsMoving(servoEnum, true);
//        while(currentAngle != desiredAngle){
//          if(currentAngle < desiredAngle && currentAngle + incrementInDegrees <= desiredAngle){
//              publish(servoEnum, currentAngle + incrementInDegrees, override);
//              currentAngle = currentAngle + incrementInDegrees;
//              Thread.sleep(stepsInMilliseconds);
//          }
//          else if(currentAngle < desiredAngle && currentAngle + incrementInDegrees > desiredAngle){
//              currentAngle = desiredAngle;
//              publish(servoEnum, desiredAngle, override);
//          }
//          else if(currentAngle > desiredAngle && currentAngle - incrementInDegrees >= desiredAngle){
//              publish(servoEnum, currentAngle - incrementInDegrees, override);
//              currentAngle = currentAngle - incrementInDegrees;
//              Thread.sleep(stepsInMilliseconds);
//          }
//          else if(currentAngle > desiredAngle && currentAngle - incrementInDegrees < desiredAngle){
//              publish(servoEnum, desiredAngle, override);
//              currentAngle = desiredAngle;
//          }
//        }
//        tracker.setIsMoving(servoEnum, false);
//    }
}
