# Important to know files:
- AMG8833_HardwareCode_Internet.py is code directly copied from the Maker Portal LLC site for the AMG8833
- AMG8833_Internet_Modified.py is code the omits the usage of matplotlib.pyplot library
- .gitignore is used to ignore files and folders that should not be pushed to Github
- __init__.py is an empty file used by Python to indicate importable files from this directory

# Hierachy of Imports for AMG8833 Usage
1. AMG8833_ErrorFind.py imports AMG8833_Initalization.py
2. AMG8833_Initialization.py imports amg8833_i2c.py
> amg8833_i2c.py is a file directly copied from Maker Portal LLC for AMG8833

# Neccessary libraries for AMG8833 operation
- {sys, time, numpy, smbus}
> smbus only works on Linux machines

# Purpose of the testing files (AMG8833_Error_Test.md & AMG8833_ErrorFind_Test.py)
- The testing program was a draft for the implementation of the AMG8833 code and to demostrate how it should behave, along with expected outputs.
- Markdown file (AMG8833_Error_Test) elaborates more on AMG8833_ErrorFind_Test.py

# Expected Usage of AMG8833_ErrorFind.py
- The file should be create an object of type "Thermal Camera"
- This object will be initialized to turn on and then awaiting further functions
- Other functions will read:
  - AMG8833 data,
  - process it to output a detected heat column (most heatmass detected in x-axis),
  - and output a boolean for firing mechanism.
