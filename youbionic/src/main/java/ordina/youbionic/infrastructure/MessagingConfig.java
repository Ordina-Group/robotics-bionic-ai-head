package ordina.youbionic.infrastructure;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;

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

    @Bean
    public RabbitTemplate template(){
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory());
        rabbitTemplate.setMessageConverter(converter());
        return rabbitTemplate;
    }

    @Bean
    public MessageConverter converter(){
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public ConnectionFactory connectionFactory() {
        return new CachingConnectionFactory(host, port);
    }
}
