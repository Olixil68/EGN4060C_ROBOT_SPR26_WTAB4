# All-in-one Program to read values from the AMG8833 and do post-processing on said values
import numpy as np
import sys
import time
# import Local Files
sys.path.append("../") # Add Local Directory
import AMG8833_Initalization # Local File

def HeatList(thermalGrid):
    heatMass_list = []

    # Apply weight of column number of heat detected
    npGrid = np.array(thermalGrid)
    for row in range(0,8):
        for col in range(0,8):
            if(npGrid[row][col] > 20):
                npGrid[row][col] = (col + 1)
                heatMass_list.append(npGrid[row][col])
            else:
                npGrid[row][col] = 0

    return heatMass_list

def HeatmassCenter(heatList):
    heatCol = 4.5
    if(len(heatList) == 0):
        heatCol = 0.0 # 0.0 is out-of-scope; no object detected
        return heatCol
    else:
        heatMass_avg = (sum(heatList) / len(heatList))
        print(f"heatMass_avg: {heatMass_avg}") # debug line
        heatCol = heatMass_avg
        return heatCol

def ReadyToFire(list):
    # variable for firing-state
    # {0 = No Target; 1 = Target}
    rtf = False
    if(len(list) == 0):
        rtf = False
        return rtf
    if(len(list) >= 21):
        rtf = True
        return rtf

if __name__ == '__main__':
    try:
        tc1 = AMG8833_Initalization.Thermal_Camera()
        tc1.Thermal_Init()
        time.sleep(1) # let sensor become stable

        tc1_array = tc1.Thermal_Read()
        print(tc1_array) # debug line

        tc1_heatList = HeatList(tc1_array)
        print(tc1_heatList) # debug line

        tc1_heatCol = HeatmassCenter(tc1_heatList)
        print(f"Heat Direction is Column {tc1_heatCol}") # debug line

        tc1_rtf = ReadyToFire(tc1_heatList)
        print(f"Good For Firing: {tc1_rtf}")
    except Exception as e:
        print(f"An error occured: {e}")
