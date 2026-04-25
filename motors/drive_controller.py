# =========================
# DRIVE CONTROLLER — STUB
# =========================
# TODO: Replace this stub with real motor/drive hardware code.
#
# Your implementation must provide a DriveController class
# with forward(), stop(), and (optionally) turn() methods.
#
# Interface contract:
#   forward()          — move robot forward continuously
#   stop()             — halt all motors immediately
#   turn(direction)    — optional: 'left' or 'right' (not yet used by main.py)
# =========================


class DriveController:
    """
    STUB — replace method bodies with real motor driver logic.

    DO NOT change the class name or method signatures —
    main.py imports and calls these exactly as shown.
    """

    def __init__(self):
        # TODO: initialise your motor controller here
        # e.g. set up GPIO pins, motor driver IC, PWM channels, etc.
        print("[DRIVE] initialised (simulation mode)")

    def forward(self):
        """
        Drive robot forward.
        TODO: set motor direction + speed via your driver.
        """
        print("[DRIVE-SIM] moving forward")

    def stop(self):
        """
        Stop all motors.
        TODO: set motor speed to 0 / engage brake.
        """
        print("[DRIVE-SIM] stopped")

    def turn(self, direction="left"):
        """
        Turn in place.  direction = 'left' | 'right'
        TODO: implement differential drive or steering servo.
        Optional — not currently called by main.py but here for your use.
        """
        print(f"[DRIVE-SIM] turning {direction}")
