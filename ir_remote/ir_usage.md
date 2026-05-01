# Important Files
- remote_controller.py is the only code to operate the Infrared Receiver
- __init__.py is to allow main.py to call the remote controller if directing importing the exact directory hierarchy from GitHub

# Important Libraries
- lgpio

# Expected Usage of remote_controller.py
- The IR sensor should be directed connected to the GPIO17 on the Raspberry PI
- The robot is set and expects to receive a signal across this pin on startup
- The robot waits until Update(void) returns True when the board reads a signal on GPIO17, else the Update(void) returns False
- The IR sensor shuts down after getting called to shut down in main.py 