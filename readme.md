# Welcome to the repository for Ordina's application for the YouBionic robothead. <br>
As it is currently still in development, there's not one application to straight-up run and get going. <br>

> [!TIP]
> A tutorial to get you started does exist! Try following it to get you up to speed ASAP :)

Or, try <br> 
* Run /message_hub/src/main/java/ordina/youbionic/YouBionicApplication.java
* Then, once that it up and running, run /servo_driver/servo_driver.py
* Then, run /sound_driver/sound_driver.py
* Then, run /microphone_driver/microphone_driver/microphone_driver.py
* Then, start the front-end by running a terminal and navigating to svelte-app and running 'npm run dev'
* Once they are both active, navigate to localhost:8080/ to try out the endpoints, or to whatever port Svelte will run on to make calls through the front-end by pressing a button.


> Current endpoints are 

- /laugh, 
- /yes, 
- /no, 
- /blink,
- /rest,
- /closeeyes,
- /openeyes,
- /sleep,
- /demo,
- /sus,
- /sound,
- /reset,
- /manualnumber/{servonumber}/{angle},
- /manualname/{servo-name}/{angle}, 
- /config{servonumber}
>[!IMPORTANT]
> {servonumber} is either 0, 1, 2, 3, 4, 5, 13, 14 or 15 <br>
> And angle is anything between 0-180.

> [!TIP]
> The possible range of angles depends on the servomotor chosen. Not every angle will be accepted.
> The application currently does not have clear indications of when this is the case. This is a to-do for a future developer :)
