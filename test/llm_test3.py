from invoke import run

command = "echo Heb je een leuk feitje voor me? | ollama run bramvanroy/fietje-2b-chat:Q3_K_M > output.txt"
run(command, hide=True, warn=True)



