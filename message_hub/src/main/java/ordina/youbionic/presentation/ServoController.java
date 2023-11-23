package ordina.youbionic.presentation;

import ordina.youbionic.infrastructure.QueueEnum;
import ordina.youbionic.infrastructure.RabbitMQPublisher;
import ordina.youbionic.service.ServoService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
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
        return service.testAll();
    }

    @PutMapping("/reset")
    public String reset() throws Exception{
        return service.reset();
    }

    @PutMapping("/laugh")
    public String laugh() throws Exception{
        return service.laugh();
    }

    @PutMapping("/config/{servo}")
    public String config(@PathVariable String servo) throws Exception{
        return service.config(servo);
    }

    @PutMapping("/manual/{servo}/{angle}")
    public String manual(@PathVariable String servo, @PathVariable String angle) throws Exception{
        return service.manual(servo, angle);
    }

    @PutMapping("/rest")
    public String rest() throws Exception{
        return service.rest();
    }

    @PutMapping("/blink")
    public String blink() throws Exception{
        service.blink();
        return "Blinked.";
    }

    @PutMapping("/yes")
    public String yes() throws Exception{
        service.nodYes();
        return "Yes.";
    }

    @PutMapping("/no")
    public String no() throws Exception{
        service.shakeNo();
        return "No.";
    }

}
