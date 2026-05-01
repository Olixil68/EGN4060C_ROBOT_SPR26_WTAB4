# Important Files
- Movement.py is the only python file for controlling the robot's wheels and controlling the LIDAR component of the robot.
- robot_arduino.cpp is not an official file for controlling the robot's wheels as the actual code written by the movement programmer was done in the Arduino IDE, meaning the offical file is an Arduino IDE sketch and is saved as an .ino file.
- __init__.py allows this whole directory to be used by the main function if directing importing directory hierarchy from GitHub

# Important Libraries
- pyserial
- time
- random
- rplidar
- All imports automatically done in Arduino IDE (i.e., <arduino.h>, etc)

# Hard-coded constants for LIDAR and Wheel operation
- LIDAR_PORT       = '/dev/rplidar'
- ARDUINO_PORT     = '/dev/arduino'
- BAUD_RATE        = 9600
- MAX_DISTANCE_MM  = 800      # mm  - ignore objects beyond this
- STOP_DISTANCE_MM = 305      # mm  - ~1 foot: stop here for thermal scan
- FRONT_TOLERANCE  = 20       # degrees - within ±20° of front = aligned
- SEARCH_DURATION  = 3.0      # seconds per random search move
- ESCAPE_DRIVE_SEC = 2.0      # seconds to drive forward after 180° turn
- MM_TO_M = 0.001             # unit conversion

# Expected usage of movement.py
- Robot connections should be attached directly to the LIDAR and Arduino board (which should be connected to wheel motor drivers)
- Arudino board should already have the code from robot_arduino.cpp -> robot_arduino.ino
- All relevant motor controls should be in the robot_arduino.ino
> Forward, Backwards, Turn Left, Turn Right, Stop, & 180Turn

- The robot should navigate in a random direction until an object is detected within its range (as set by MAX_DISTANCE_MM)
- During this same movement step, the robot will be sending LIDAR pulses until an object is detected within its range
- The robot will call the LIDAR to send for a distance and angle from the detected object
- It will move and align the robot until the detected object is aligned by the FRONT_TOLERANCE of the front portion of the LIDAR and is within the STOP_DISTANCE_MM of the detected object.
- It will wait until Thermal Camera code is called before either returning to randomly navigate or do a 180 degree turn depending on output of Thermal Camera:
> If Thermal_Camera(validTarget) == True,
  > Then Firing(void)
  > Then RandomMove(void)
> If Thermal_Camera(validTarget) == False,
  > Then Escape180(void)
- Finally, LIDAR and Wheel motors will shutdown after getting called to shut down in main.py


