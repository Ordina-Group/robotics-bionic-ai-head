package ordina.youbionic.infrastructure;

import org.springframework.amqp.core.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MessagingConfig {
    @Value("localhost")
    private String host;

    @Value("5672")
    private int port;
    @Value("ServoControlBindingKey")
    private String servoKey;

    @Bean
    public Queue servoQueue(){return QueueBuilder.durable("servoQueue").build();}

    @Bean
    public TopicExchange topicExchange(){
        return new TopicExchange("topicExchange");
    }

    @Bean
    public Binding servoBinding(){
        return BindingBuilder.bind(servoQueue()).to(topicExchange()).with(servoKey);
    }
}
