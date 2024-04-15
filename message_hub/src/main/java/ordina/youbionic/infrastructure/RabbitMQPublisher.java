package ordina.youbionic.infrastructure;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import ordina.youbionic.exception.IllegalEnumValueException;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class RabbitMQPublisher {
    private final Channel channel;

    public RabbitMQPublisher() throws Exception{
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        factory.setPort(5672);
        Connection connection = factory.newConnection();
        this.channel = connection.createChannel();
        channel.queueDeclare("servo", false, false, false, null);
        channel.queueDeclare("audio_input", false, false, false, null);
        channel.queueDeclare("audio_output", false, false, false, null);
        channel.queuePurge("servo");
    }

    // We work using an Enum for the queue, in order to reduce error rates.
    public void publish(final QueueEnum queueEnum, final String message) throws IllegalEnumValueException{
        String queue_name;
        switch (queueEnum) {
            case SERVO:
                queue_name = "servo";
                break;
            case AUDIO_INPUT:
                queue_name = "audio_input";
                break;
            case AUDIO_OUTPUT:
                queue_name = "audio_output";
                break;
            default:
                throw new IllegalEnumValueException("Attempted to publish message to the wrong queue.");
        }
        try {
            channel.basicPublish("", queue_name, null, message.getBytes());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void purge(final QueueEnum queueEnum) throws IOException {
        String queue = switch(queueEnum){
            case SERVO -> "servo";
            case AUDIO_INPUT -> "audio_input";
            case AUDIO_OUTPUT -> "audio_output";
        };
        channel.queuePurge(queue);
    }

}
