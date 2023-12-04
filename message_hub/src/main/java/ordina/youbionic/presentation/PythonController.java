package ordina.youbionic.presentation;

import java.io.IOException;

public class PythonController {
    // TODO: Make sure the path-to-python-file gets fixed
    private ProcessBuilder pb = new ProcessBuilder("python", "path-to-python-file.py");
    private Process pythonProcess;

    public PythonController() {
    }

    public void startPython() throws IOException {
        this.pythonProcess = pb.start();
    }
    public void killPython(){
        this.pythonProcess.destroy();
    }

    public void restartPython() throws IOException {
        killPython();
        startPython();
    }
}
