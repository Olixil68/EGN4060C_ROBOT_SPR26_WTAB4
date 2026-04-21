# Please see AMG8833_Error_Test.md file to see testing documentation
import numpy as np

# Apply a weight to every cell of the grid
# Return an error column based on heatMass average column and center of 8x8 grid
def gridErrorSolver(grid):
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
    gridPrinter(npGrid) # debug line
    print(f"heatmass_list: {heatmass_list}") # debug line

    # Find the heatmass average
    if(len(heatmass_list) == 0):
        print("heatmap_list is empty") # debug line
        heatCol = 0.0
        return heatCol
    else:
        heatmass_avg = (sum(heatmass_list) / len(heatmass_list))
        print(f"heatmass_avg: {heatmass_avg}") # debug line

    # Find Heat Column
    heatCol = heatmass_avg
    return heatCol

# Prints each cell of the grid
def gridPrinter(grid):   
    for row in grid:
        print(*row, sep="\t")

if __name__ == '__main__':
    # Empty case
    grid1 = [
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 24),
            ]
    # Right-focused
    grid2 = [
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 24, 24, 24, 24, 32),
            (24, 24, 24, 24, 24, 24, 32, 32),
            (24, 24, 24, 24, 24, 32, 32, 32),
            (24, 24, 24, 24, 24, 32, 32, 32),
            (24, 24, 24, 24, 24, 32, 32, 32),
            (24, 24, 24, 24, 24, 24, 32, 32),
            (24, 24, 24, 24, 24, 24, 32, 32),
            ]
    # Center-focused
    grid3 = [
            (24, 24, 24, 24, 24, 24, 24, 24),
            (24, 24, 24, 32, 32, 24, 24, 24),
            (24, 24, 32, 32, 32, 32, 24, 24),
            (24, 24, 32, 32, 32, 32, 24, 24),
            (24, 24, 32, 32, 32, 32, 24, 24),
            (24, 24, 24, 32, 32, 24, 24, 24),
            (24, 24, 24, 32, 32, 24, 24, 24),
            (24, 24, 24, 32, 32, 24, 24, 24),
            ]
    # Left-focused
    grid4 = [
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            (32, 32, 24, 24, 24, 24, 24, 24),
            ]
    
    heatMass_dir = gridErrorSolver(grid1)
    print(f"Heat Mass Direction is {heatMass_dir}")

    HM2 = gridErrorSolver(grid2)
    print(f"HM2: {HM2}")

    HM3 =  gridErrorSolver(grid3)
    print(f"HM3: {HM3}")

    HM4 =  gridErrorSolver(grid4)
    print(f"HM4: {HM4}")