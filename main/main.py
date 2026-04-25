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
#   remote_controller.py   IR sensor on ADC A0
#   fire_controller.py     Servo via robot_hat I2C
#   thermal_camera.py      AMG8833 via I2C + ErrorFind scoring
#   amg8833_i2c.py         Low-level I2C driver (provided separately)
#
# Teammate stub modules (in SIM/ -- replace bodies when ready):
#   SIM/lidar_controller.py    LidarController
#   SIM/drive_controller.py    DriveController
# =========================

import time

from remote_controller    import RemoteController
from fire_controller      import FireController
from amg8833              import thermal_camera
from SIM.lidar_controller import LidarController
from SIM.drive_controller import DriveController

# -----------------------------------------------------------------------
# AMBIENT TEMPERATURE
# ThermalCamera returns a "Fire" State based on number of hot pixels:
# The check for hot pixels is based on environmental ambient temperature
# Change this one value to adjust sensitivity.
# -----------------------------------------------------------------------
AMBIENT_TEMP = 20.0

class Robot:

    def __init__(self):

        print("[SYSTEM] BOOTING ROBOT")

        self.remote  = RemoteController()   # ADC A0, no GPIO pin needed
        self.fire    = FireController()

        self.thermal = thermal_camera.ThermalCamera()
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
                validTarget = thermal_camera.ReadyToFire(grid, AMBIENT_TEMP)
                if validTarget:
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