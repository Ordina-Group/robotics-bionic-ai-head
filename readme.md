# Welcome to the repository for Ordina's application for the YouBionic robothead. <br>
As it is currently still in development, there's not one application to straight-up run and get going. <br>

Instead, try <br> 
* Run /message_hub/src/main/java/ordina/youbionic/YouBionicApplication.java 
* Then, once that it up and running, run /servo_driver/servo_driver.py
* Once they are both active, navigate to localhost:8080/ to try out the endpoints.


> Current endpoints are 

- /laugh, 
- /yes, 
- /no, 
- /blink, 
- /manual/{servonumber}/{angle}, 
- /config{servonumber}
>[!IMPORTANT]
> {servonumber} is either 0, 1, 2, 3, 4, 5, 13, 14 or 15 <br>
> And angle is anything between 0-180.

> [!TIP]
> The possible range of angles depends on the servomotor chosen. Not every angle will be accepted.
> The application currently does not have clear indications of when this is the case. This is a feature soon to be added.
