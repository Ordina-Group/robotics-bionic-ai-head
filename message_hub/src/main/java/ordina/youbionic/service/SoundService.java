package ordina.youbionic.service;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.exception.IllegalEnumValueException;
import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class SoundService {
    private final RabbitMQPublisher publisher;

    public SoundService(){
        try {
            this.publisher = new RabbitMQPublisher();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void playSound(){
      publish("play_sound");

    private void publish(final String message) throws IllegalEnumValueException {
        publisher.publish(QueueEnum.AUDIO_OUTPUT, message);
    }
}
