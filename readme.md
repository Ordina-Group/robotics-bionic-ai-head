Welcome to the repository for Ordina's application for the YouBionic robothead.
As it is currently still in development, there's no one application to straight-up run and get going.
Instead; 
Run /message_hub/src/main/java/ordina/youbionic/YouBionicApplication.java
Then, once that it up and running, run /servo_driver/servo_driver.py
Once they are both active, navigate to localhost:8080/ to try out the endpoints.
Current endpoints are /laugh, /yes, /no, /blink, /manual/{servonumber}/{angle}, /config{servonumber}
                                                Where {servonumber} is either 0, 1, 2, 3, 4, 5, 13, 14 or 15, and angle is                                                                                         anything between 0-180.
:)
