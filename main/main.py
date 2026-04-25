# =========================
# MAIN — ROBOT STATE MACHINE
# =========================
# Coordinates all subsystems through a 6-state machine:
#
#   IDLE      wait for IR remote start signal
#   SEARCH    drive forward + LIDAR scan for objects
#   APPROACH  close in until object is within 3.0 m
#   THERMAL   confirm target with AMG8833 heat camera
#   FIRE      execute servo firing sequence
#   COOLDOWN  2-second pause, then return to SEARCH
#
# Real hardware modules (yours):
#   remote_controller.py   IR sensor on GPIO 17
#   fire_controller.py     Servo on GPIO 18
#   thermal_camera.py      AMG8833 via I2C + ErrorFind scoring
#   amg8833_i2c.py         Low-level I2C driver (provided separately)
#
# Teammate stub modules (in SIM/ -- replace bodies when ready):
#   SIM/lidar_controller.py    LidarController
#   SIM/drive_controller.py    DriveController
#
# When hardware is absent (no RPi, no I2C), every module silently falls
# back to a software simulation so the full loop can be tested on a laptop.
# =========================

import time

from remote_controller    import RemoteController
from fire_controller      import FireController
from thermal_camera       import ThermalCamera, ErrorFind
from SIM.lidar_controller import LidarController
from SIM.drive_controller import DriveController

# -----------------------------------------------------------------------
# FIRE THRESHOLD
# ErrorFind returns the weighted average COLUMN (1-8) of hot pixels:
#   ~1-2 = heat on the left
#   ~4-5 = heat centred
#   ~6-8 = heat on the right / centre-right
# Change this one value to adjust sensitivity.
# -----------------------------------------------------------------------
FIRE_THRESHOLD = 6.0


class Robot:

    def __init__(self):

        print("[SYSTEM] BOOTING ROBOT")

        self.remote  = RemoteController(pin=17)
        self.fire    = FireController(pin=18)

        self.thermal = ThermalCamera()
        try:
            self.thermal.init()
            print("[THERMAL] initialised successfully")
        except Exception as e:
            print(f"[THERMAL] initialisation failed: {e}")

        self.lidar = LidarController()
        self.drive = DriveController()

        self.state = "IDLE"
        print("[SYSTEM] READY - waiting for IR start signal")

    def run(self):

        while True:

            if self.state == "IDLE":
                print("[STATE] IDLE")
                if self.remote.update():
                    print("[IR] START RECEIVED")
                    self.state = "SEARCH"

            elif self.state == "SEARCH":
                print("[STATE] SEARCH")
                self.drive.forward()
                detected, distance = self.lidar.detect()
                if detected:
                    print(f"[LIDAR] object detected at {distance:.2f} m")
                    self.state = "APPROACH"
                time.sleep(0.2)

            elif self.state == "APPROACH":
                print("[STATE] APPROACH")
                self.drive.forward()
                detected, distance = self.lidar.detect()
                if distance is not None and distance <= 3.0:
                    print(f"[LIDAR] target in range ({distance:.2f} m) - stopping")
                    self.drive.stop()
                    self.state = "THERMAL"
                time.sleep(0.2)

            elif self.state == "THERMAL":
                print("[STATE] THERMAL CHECK")
                grid  = self.thermal.read()
                score = ErrorFind(grid)
                print(f"[THERMAL] score = {score:.2f}  (threshold = {FIRE_THRESHOLD})")
                if score >= FIRE_THRESHOLD:
                    print("[THERMAL] VALID TARGET CONFIRMED")
                    self.state = "FIRE"
                else:
                    print("[THERMAL] no valid target - returning to search")
                    self.state = "SEARCH"

            elif self.state == "FIRE":
                print("[STATE] FIRE")
                self.drive.stop()
                self.fire.fire()
                self.state = "COOLDOWN"

            elif self.state == "COOLDOWN":
                print("[STATE] COOLDOWN")
                time.sleep(2)
                self.state = "SEARCH"


if __name__ == "__main__":
    robot = Robot()
    robot.run()