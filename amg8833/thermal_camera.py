# =========================
# THERMAL CAMERA (AMG8833)
# =========================
# Provides ThermalCamera and ErrorFind to main.py.
#
# ThermalCamera wraps the real AMG8833 hardware class and falls back
# to a software simulation automatically when the hardware / i2c driver
# is not present (e.g. running on a laptop for testing).
#
# ErrorFind is the heat-column scoring function written by your teammate.
# It returns a float in [0.0, 8.0]:
#   0.0        = ambient (nothing warm detected)
#   1.0 – 8.0  = weighted average column of the heat mass
#                (1 = far left, 8 = far right, ~4.5 = centred)
#
# main.py fires when ErrorFind returns >= 6  (heat mass on the right half).
# =========================

import time
import sys
import numpy as np

# ---------------------------------------------------------------------------
# Try to import the real AMG8833 i2c driver.
# The driver file (amg8833_i2c.py) must be in the project root or on sys.path.
# ---------------------------------------------------------------------------
try:
    import amg8833_i2c
    _HARDWARE_AVAILABLE = True
except ImportError:
    _HARDWARE_AVAILABLE = False


# ===========================================================================
# LOW-LEVEL HARDWARE READER  (your teammate's Thermal_Camera, tidied up)
# ===========================================================================

class _AMG8833HardwareReader:
    """
    Wraps amg8833_i2c.AMG8833 with init / read methods.
    Tries I2C address 0x69 first (AD0=5V), then 0x68 (AD0=GND).
    """

    def __init__(self):
        self.sensor = None

    def init(self):
        """Block up to 1 second while sensor starts, then settle for 100 ms."""

        t0 = time.time()
        while (time.time() - t0) < 1.0:
            try:
                self.sensor = amg8833_i2c.AMG8833(addr=0x69)
                break
            except Exception:
                try:
                    self.sensor = amg8833_i2c.AMG8833(addr=0x68)
                    break
                except Exception:
                    pass

        time.sleep(0.1)  # let sensor settle

        if self.sensor is None:
            print("[THERMAL] No AMG8833 found - check wiring and I2C address")
            sys.exit(1)

    def read(self):
        """
        Return an 8x8 numpy array of pixel temperatures in °C.
        Retries automatically if the sensor reports a pixel error.
        """

        pix_res     = (8, 8)
        pix_to_read = 64

        while True:
            status, pixels = self.sensor.read_temp(pix_to_read)
            if status:      # sensor flagged an error - retry
                continue
            return np.reshape(pixels, pix_res)


# ===========================================================================
# SIMULATION FALLBACK
# ===========================================================================

class _AMG8833SimReader:
    """
    Pure-software simulation of the AMG8833.
    Used automatically when the real i2c driver is absent.
    Produces realistic warm blobs so the full state machine can be tested.
    """

    def init(self):
        print("[THERMAL-SIM] no hardware found - running in simulation mode")

    def read(self):
        import random

        AMBIENT = 22.0
        grid = np.full((8, 8), AMBIENT)

        # 60% chance of a warm blob (simulates a person in view)
        if random.random() < 0.6:
            cx = random.randint(1, 6)
            cy = random.randint(1, 6)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    r, c = cx + dx, cy + dy
                    if 0 <= r < 8 and 0 <= c < 8:
                        grid[r][c] += random.uniform(6.0, 14.0)

        return grid


# ===========================================================================
# PUBLIC INTERFACE - ThermalCamera
# ===========================================================================

class ThermalCamera:
    """
    Interface used by main.py:

        cam = ThermalCamera()
        cam.init()
        grid = cam.read()   # returns 8x8 numpy array of degrees C values
    """

    def __init__(self):
        if _HARDWARE_AVAILABLE:
            self._reader = _AMG8833HardwareReader()
            print("[THERMAL] hardware driver loaded")
        else:
            self._reader = _AMG8833SimReader()
            print("[THERMAL] simulation driver loaded (amg8833_i2c not found)")

    def init(self):
        self._reader.init()

    def read(self):
        return self._reader.read()


# ===========================================================================
# ErrorFind  - teammate's heat-column scoring algorithm
# ===========================================================================

def ErrorFind(grid):
    """
    Scores an 8x8 thermal grid and returns the weighted average column
    of pixels that exceed ambient temperature (> 24 degrees C).

    Algorithm (from teammate's AMG8833_ErrorFind.py):
      1. For each pixel hotter than 24 degrees C, record its 1-based column
         number (1 = leftmost, 8 = rightmost).
      2. Collect all such column-weights into a list.
      3. Return the average of that list  ->  range [1.0, 8.0]
         If no hot pixels exist, return 0.0 (ambient scene).

    The return value tells main.py WHERE heat is on the grid:
      ~1-2  far left  |  ~4-5  centre  |  ~7-8  far right

    main.py fires when the score >= 6 (heat mass on right / centre-right).
    Your team can adjust that threshold in main.py as needed.

    Args:
        grid: 8x8 array-like of temperatures in degrees C
              (numpy array or list-of-lists both work)

    Returns:
        float  0.0 (ambient) or 1.0-8.0 (weighted column average)
    """

    AMBIENT_THRESHOLD = 24  # degrees C - pixels above this count as heat

    heatmass_list = []
    npGrid = np.array(grid)

    for row in range(8):
        for col in range(8):
            if npGrid[row][col] > AMBIENT_THRESHOLD:
                # weight = 1-based column index
                heatmass_list.append(col + 1)

    # no heat detected - ambient scene
    if len(heatmass_list) == 0:
        return 0.0

    heatmass_avg = sum(heatmass_list) / len(heatmass_list)

    print(f"[THERMAL] hot pixels: {len(heatmass_list)}  |  "
          f"heatmass_avg column: {heatmass_avg:.2f}")

    return heatmass_avg


# ===========================================================================
# Optional helper - kept for debug / standalone testing
# ===========================================================================

def gridPrinter(grid):
    """Print the 8x8 grid to console in a readable format."""
    npGrid = np.array(grid)
    for row in npGrid:
        print("\t".join(f"{v:5.1f}" for v in row))
