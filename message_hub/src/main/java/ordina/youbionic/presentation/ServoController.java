package ordina.youbionic.presentation;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.service.ServoService;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
//    @RequiredArgsConstructor
public class ServoController {
    private final ServoService service;

    public ServoController(){
        this.service = new ServoService();
    }

    @PutMapping("/reset")
    public String reset() throws Exception{
        service.reset();
        return "All servomotors reset to 90 degrees and ready for assembly!";
    }

    @PutMapping("/laugh")
    public String laugh() throws Exception{
        service.laugh();
        return "Hahahaha";
    }

    @PutMapping("/configure/{servo}")
    public String configure(@PathVariable int servo) throws Exception{
        return service.configure(servo);
    }

    @PutMapping("/manual/{servo}/{angle}")
    public String manual(@PathVariable int servo, @PathVariable int angle) throws Exception{
        return service.manual(servo, angle);
    }

    @PutMapping("/rest")
    public String rest() throws Exception{
        service.rest();
        return "Head returned to resting position";
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
