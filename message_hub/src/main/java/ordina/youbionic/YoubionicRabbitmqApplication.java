package ordina.youbionic;

//import jakarta.annotation.PreDestroy;
//import ordina.youbionic.presentation.PythonController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class YoubionicRabbitmqApplication {
//	private static final PythonController pythonController = new PythonController();

	public static void main(String[] args) {
		SpringApplication.run(YoubionicRabbitmqApplication.class, args);
//		pythonController.startPython();
	}

//	@PreDestroy
//	public void onExit(){
//		pythonController.killPython();
//	}
//
//	public void restartPython(){
//		pythonController.restartPython();
//	}



}
