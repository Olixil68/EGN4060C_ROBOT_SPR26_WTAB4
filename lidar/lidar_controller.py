# =========================
# LIDAR CONTROLLER — STUB
# =========================
# TODO: Replace this stub with real LIDAR hardware code.
#
# Your implementation must provide a LidarController class
# with a detect() method matching the interface below.
#
# Interface contract:
#   detect() -> (detected: bool, distance: float | None)
#
#   detected  — True if an object is in range, False otherwise
#   distance  — distance in metres if detected, else None
#
# The state machine uses distance <= 3.0 m as the "in range" threshold.
# =========================

import random


class LidarController:
    """
    STUB — replace body of detect() with real LIDAR logic.

    DO NOT change the class name or method signature —
    main.py imports and calls this exactly as shown.
    """

    def __init__(self):
        # TODO: initialise your LIDAR hardware here
        # e.g. open serial port, configure sensor, etc.
        print("[LIDAR] initialised (simulation mode)")

    def detect(self):
        """
        Poll the LIDAR sensor.

        Returns:
            (bool, float | None)
            detected  — True if object found
            distance  — metres to object, or None if nothing detected
        """

        # --------------------------------------------------
        # TODO: replace simulation below with real sensor read
        # --------------------------------------------------
        detected = random.choice([True, False, False])           # ~33% hit rate
        distance = round(random.uniform(0.5, 8.0), 2) if detected else None

        if detected:
            print(f"[LIDAR-SIM] object at {distance:.2f}m")

        return detected, distance
