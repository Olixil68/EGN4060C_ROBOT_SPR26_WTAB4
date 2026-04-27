# =========================
# MAIN — ROBOT STATE MACHINE
# =========================
# Coordinates all subsystems through a 7-state machine:
#
#   IDLE      wait for IR remote start signal
#   SEARCH    random search pattern + LIDAR scanning for objects
#   APPROACH  align and close in until object is within ~1 ft (305 mm)
#   THERMAL   confirm target with AMG8833 heat camera
#   FIRE      execute servo firing sequence
#   COOLDOWN  2-second pause, then return to SEARCH
#   ESCAPE    180° turn + drive away after cold target (box), then SEARCH
#
# Hardware modules:
#   remote_controller.py   IR sensor on ADC A0
#   fire_controller.py     Servo via robot_hat I2C
#   thermal_camera.py      AMG8833 via I2C + ReadyToFire scoring
#   amg8833_i2c.py         Low-level I2C driver
#   movement.py            LIDAR + Arduino serial (MovementController)
# =========================

import time

from remote_controller import RemoteController
from fire_controller   import FireController
import thermal_camera
from movement          import MovementController

# -----------------------------------------------------------------------
# AMBIENT TEMPERATURE
# ThermalCamera.ReadyToFire fires when >= 21 pixels exceed this threshold.
# Adjust to match your environment before the demo.
# -----------------------------------------------------------------------
AMBIENT_TEMP = 20.0


class Robot:

    def __init__(self):
        print("[SYSTEM] BOOTING ROBOT")

        self.remote = RemoteController()
        self.fire   = FireController()

        self.thermal = thermal_camera.ThermalCamera()
        try:
            self.thermal.init()
            print("[THERMAL] initialised successfully")
        except Exception as e:
            print(f"[THERMAL] initialisation failed: {e}")

        self.movement = MovementController()
        try:
            self.movement.connect()
            print("[MOVEMENT] initialised successfully")
        except Exception as e:
            print(f"[MOVEMENT] initialisation failed: {e}")

        self.state = "IDLE"
        print("[SYSTEM] READY - waiting for IR start signal")

    # --------------------------------------------------
    # CLEAN SHUTDOWN
    # --------------------------------------------------
    def shutdown(self):
        print("[SYSTEM] SHUTTING DOWN")

        try:
            self.movement.disconnect()
        except Exception:
            pass

        try:
            self.fire.cleanup()
        except Exception:
            pass

        print("[SYSTEM] SAFE EXIT COMPLETE")

    # --------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------
    def run(self):

        try:
            while True:

                # ==============================
                # IDLE — wait for IR start
                # ==============================
                if self.state == "IDLE":
                    print("[STATE] IDLE")
                    if self.remote.update():
                        print("[IR] START RECEIVED")
                        self.movement.reset_search()
                        self.state = "SEARCH"

                # ==============================
                # SEARCH — random pattern until LIDAR detects object
                # ==============================
                elif self.state == "SEARCH":
                    print("[STATE] SEARCH")
                    detected, distance_m, aligned = self.movement.search_tick()
                    if detected:
                        print(f"[LIDAR] object detected at {distance_m:.2f} m")
                        self.state = "APPROACH"
                    time.sleep(0.1)

                # ==============================
                # APPROACH — rotate to face, then drive to ~1 ft
                # ==============================
                elif self.state == "APPROACH":
                    print("[STATE] APPROACH")
                    in_position, detected, distance_m, aligned = self.movement.approach_tick()

                    if not detected:
                        print("[LIDAR] target lost - returning to SEARCH")
                        self.movement.reset_search()
                        self.state = "SEARCH"
                    elif in_position:
                        print(f"[LIDAR] target in range ({distance_m:.2f} m) - stopping")
                        self.state = "THERMAL"

                    time.sleep(0.1)

                # ==============================
                # THERMAL — confirm heat signature
                # ==============================
                elif self.state == "THERMAL":
                    print("[STATE] THERMAL CHECK")
                    grid        = self.thermal.read()
                    validTarget = thermal_camera.ReadyToFire(grid, AMBIENT_TEMP)

                    if validTarget:
                        print("[THERMAL] VALID TARGET CONFIRMED")
                        self.state = "FIRE"
                    else:
                        print("[THERMAL] no valid target - escaping")
                        self.state = "ESCAPE"

                # ==============================
                # FIRE — shoot water
                # ==============================
                elif self.state == "FIRE":
                    print("[STATE] FIRE")
                    self.fire.fire()
                    self.state = "COOLDOWN"

                # ==============================
                # COOLDOWN — brief pause, then back to SEARCH
                # (robot will immediately re-detect the box if still there,
                #  thermal scan will fail, ESCAPE will handle it)
                # ==============================
                elif self.state == "COOLDOWN":
                    print("[STATE] COOLDOWN")
                    time.sleep(2)
                    self.movement.reset_search()
                    self.state = "SEARCH"

                    # ==============================
                    # NOTE: for single-shot test mode, replace the two
                    # lines above with:
                    #   print("[SYSTEM] TEST COMPLETE — SHUTTING DOWN")
                    #   self.shutdown()
                    #   return
                    # ==============================

                # ==============================
                # ESCAPE — cold target (box): 180° turn + drive away
                # ==============================
                elif self.state == "ESCAPE":
                    print("[STATE] ESCAPE")
                    self.movement.escape()          # blocks ~4 seconds
                    self.movement.reset_search()
                    self.state = "SEARCH"

        except KeyboardInterrupt:
            print("\n[SYSTEM] Ctrl+C received")
            self.shutdown()


if __name__ == "__main__":
    robot = Robot()
    robot.run()