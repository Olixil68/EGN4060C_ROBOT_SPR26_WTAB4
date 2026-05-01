# This is the documentation explaining the purpose, usage, and outputs of the AMG8833_ErrorFind_Test
- If the actual program for the AMG8833 ErrorFind does not operate as expected, this document should outline the inputs and outputs that are expected.

- There are 4 generic test cases outlining what the Thermal Camera ErrorFind Function should do for the actual module: a center-focused test, a left-focused test, a right-focused test, and ambient environment test.
- This program does not utilize any user-inputted prompt
- The debug outputs for the function are stated here: 
  - The weighted grid output
  > Essentially, if a read temperature exceeds ambient environment temperature reading, then mark said pixel with the weight of the column {1-8}
  - The array containing all marked cells that exceed the ambient environment temperature
  > Once a cell is read to be higher than ambient temperature, it is added to this array
  - Prints if there is enough heatmass detected on the thermal camera for firing
  > If the heatmass array contains at least 32 entries, prints ("Ready to fire")
  - The average of the marked cell array
  > Sum the values of each array index and divided by the length of the array
  - The actual output of the official ErrorFind program
  > The output is a floating-point value that ranges from {1, 8} inclusive.
  > If the output is 0.0, then the measured environment is ambient.