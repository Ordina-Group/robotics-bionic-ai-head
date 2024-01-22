package ordina.youbionic.presentation;

import lombok.RequiredArgsConstructor;
import ordina.youbionic.service.ServoService;
import ordina.youbionic.service.SoundService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class ServoController {
    private final ServoService service;
    private final SoundService soundService;

    @GetMapping("/reset")
    public void reset() throws Exception{
        service.reset();
    }

    @GetMapping("/laugh")
    public void laugh() throws Exception{
        service.laugh();
    }

    @GetMapping("/configure/{servo}")
    public String configure(@PathVariable int servo) throws Exception{
        return service.configure(servo);
    }

    @GetMapping("/manualnumber/{servo}/{angle}")
    public String manualWithNumber(@PathVariable int servo, @PathVariable int angle) throws Exception{
        return service.manualWithNumber(servo, angle);
    }

    @GetMapping("/manualname/{servo}/{angle}")
    public String manualWithName(@PathVariable String servo, @PathVariable int angle) throws Exception{
        return service.manualWithName(servo, angle);
    }

    @GetMapping("/rest")
    public void rest() throws Exception{
        service.rest();
    }

    @GetMapping("/closeeyes")
    public void closeEyes() throws Exception{
        service.closeEyes();
    }

    @GetMapping("/openeyes")
    public void openEyes() throws Exception{
        service.openEyes();
    }

    @GetMapping("/blink")
    public void blink() throws Exception{
        service.blink();
    }

    @GetMapping("/yes")
    public void yes() throws Exception{
        service.nodYes();
    }

    @GetMapping("/no")
    public void no() throws Exception{
        service.shakeNo();
    }

    @GetMapping("/sound")
    public void playSound() throws Exception{
        soundService.playSound();
    }
}
