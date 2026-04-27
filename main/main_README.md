# Main.py libraries and components
main.py creates an object for each component and initializes them. 
- remote_controller
    - Infrared Receiver & Remote
- fire_controller.py
    - Firing Mechanism Servo
- thermal_camera.py
    - Thermal Camera
- movement.py
    - Wheel Motors and LIDAR

# Main.py libraries and files needed in root/ and VENV path
- smbus
&gt; must be installed on a linux machine
- sys
- time
- amg8833_i2c.py (Local File)
- numpy
- rplider (rplidar-robotica)
- serial (pyserial)
- lgpio
&gt; must be installed on a linux machine

# Main.py internal states
main utilizes different component objects based on its internal operation state:
&gt; main iterates down the list below until program is halted by user
- IDLE      wait for IR remote start signal
- SEARCH    random search pattern + LIDAR scanning for objects
- APPROACH  align and close in until object is within ~1 ft (305 mm)
- THERMAL   confirm target with AMG8833 heat camera
- FIRE      execute servo firing sequence
- COOLDOWN  2-second pause, then return to SEARCH
- ESCAPE    180° turn + drive away after cold target (box), then SEARCH

