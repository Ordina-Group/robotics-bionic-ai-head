package ordina.youbionic.presentation;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.service.ServoService;
import ordina.youbionic.service.SoundService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class MessageController {
    private final ServoService servoService;
    private final SoundService soundService;

    @GetMapping("/reset")
    public void reset() throws Exception{
        servoService.reset();
    }

    @GetMapping("/laugh")
    public void laugh() throws Exception{
        servoService.laugh();
        soundService.laugh();
    }

    @GetMapping("/configure/{servo}")
    public String configure(@PathVariable int servo) throws Exception{
        return servoService.configure(servo);
    }

    @GetMapping("/manualnumber/{servo}/{angle}")
    public String manualWithNumber(@PathVariable int servo, @PathVariable int angle) throws Exception{
        return servoService.manualWithNumber(servo, angle);
    }

    @GetMapping("/manualname/{servo}/{angle}")
    public String manualWithName(@PathVariable String servo, @PathVariable int angle) throws Exception{
        return servoService.manualWithName(servo, angle);
    }

    @GetMapping("/rest")
    public void rest() throws Exception{
        servoService.rest();
    }

    @GetMapping("/closeeyes")
    public void closeEyes() throws Exception{
        servoService.closeEyes();
    }

    @GetMapping("/sleep")
    public void sleep() throws Exception{
        servoService.sleep();
    }

    @GetMapping("/demo")
    public void demo() throws Exception{
        servoService.demo();
		soundService.demo();
    }

    @GetMapping("/sus")
    public void sus() throws Exception{
        servoService.sus();
    }

    @GetMapping("/openeyes")
    public void openEyes() throws Exception{
        servoService.openEyes();
    }

    @GetMapping("/blink")
    public void blink() throws Exception{
        servoService.blink();
    }

    @GetMapping("/yes")
    public void yes() throws Exception{
        servoService.nodYes();
    }

    @GetMapping("/no")
    public void no() throws Exception{
        servoService.shakeNo();
    }

    @GetMapping("/sound")
    public void playSound() throws Exception{
        soundService.playSound();
    }

}
