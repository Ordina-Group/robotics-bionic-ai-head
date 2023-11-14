package ordina.youbionic.presentation;

import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import ordina.youbionic.service.ServoService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ServoController {
    private final ServoService service;

    public ServoController(){
        this.service = new ServoService();
    }

    @GetMapping("/test0")
    public String test0() throws Exception{
        return service.test0();
    }

    @GetMapping("/test1")
    public String test1() throws Exception{
        RabbitMQPublisher publisher = new RabbitMQPublisher();
        publisher.publish(QueueEnum.SERVO, "15,180,0");
        publisher.publish(QueueEnum.SERVO, "14,180,0");
        Thread.sleep(400);
        publisher.publish(QueueEnum.SERVO, "15,0,0");
        publisher.publish(QueueEnum.SERVO, "14,0,0");
        return "Great success";
    }

    @GetMapping("/reset")
    public String reset() throws Exception{
        return service.reset();
    }
}
