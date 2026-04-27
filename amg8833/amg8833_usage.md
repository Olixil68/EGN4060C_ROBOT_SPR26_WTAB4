# Important to know files:
- \[archived\]AMG8833_Initialization.py code logic is used for thermal_camera._AMG8833HardwareReader()
- \[archived\]AMG8833_ErrorFind.py code logic is used for thermal_camera.ReadyToFire()
- amg8833_i2c.py is Hardware-level code to utilize the AMG8833
&gt; amg8833_i2c.py is a file directly copied from Maker Portal LLC for AMG8833

# Neccessary libraries for AMG8833 operation
- {sys, time, numpy, smbus}
&gt; smbus only works on Linux machines

# Expected Usage of thermal_camera.py
- The file should be create an object of type "Thermal Camera"
- This object will be initalized with the Hardware code or with a Simulator code
- Other functions will be:
  - read AMG8833 data,
  - process the AMG8833 data to detect heated pixels
  - and output a boolean for firing mechanism.
