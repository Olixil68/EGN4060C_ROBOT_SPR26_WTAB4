# Important Files
- fire_controller.py is the current code that is utilized by main.py
> This file combines both turning the servo_on and the servo_off in the same function
- firing.py is a functionally duplicate code that is significantly smaller in size
> This file has the servo_on and servo_off functions separate and must both be called by main.py if this file is used in main.py 
- __init__.py allows main.py to call the firing code when directing importing the exact Directory Hierarchy from GitHub

# Important Libraries
- robot_hat (Sunfounder Robot Hat)
- time

# Expected usage of fire_controller.py
- Main.py calls the firing code 
- Firing code sets the servo to ON to activate the Gel Blaster for a few moments before turning the servo to OFF
- Finally, it turns off by ensuring the servo is in the OFF state