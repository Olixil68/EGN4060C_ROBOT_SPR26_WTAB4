# All-in-one Program to read values from the AMG8833 and do post-processing on said values
import numpy as np
import sys
# import Local Files
sys.path.append("C:\Users\lifit\Local_Documents\Python Files\EGN4060C-LAB") # Add Local Directory
import AMG8833_Initalization # Local File

def ErrorFind(grid):
    heatCol = 4.5
    heatmass_list = []

    # Apply weight of column number of heat detected
    npGrid = np.array(grid)
    for row in range(0,8):
        for col in range(0,8):
            if(npGrid[row][col] > 24):
                npGrid[row][col] = (col + 1)
                heatmass_list.append(npGrid[row][col])
            else:
                npGrid[row][col] = 0

    # Find the heatmass average
    if(len(heatmass_list) == 0):
        heatCol = 0.0
        return heatCol
    else:
        heatmass_avg = (sum(heatmass_list) / len(heatmass_list))
        print(f"heatmass_avg: {heatmass_avg}") # debug line

    # Find Heat Column
    heatCol = heatmass_avg
    return heatCol

if __name__ == '__main__':
    try:
        tc1 = AMG8833_Initalization.Thermal_Camera()
        tc1.Thermal_Init()
        tc1_array = tc1.Thermal_Read()
        tc1_error = ErrorFind(tc1_array)

    except Exception as e:
        print(f"An error occured: {e}")
