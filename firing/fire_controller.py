# =========================
# FIRE CONTROLLER (SERVO) — HARDWARE ONLY
# =========================
# NO simulation mode. NO fallback.
# If robot_hat is missing or broken → program crashes immediately.

import time

from robot_hat import Servo  # crashes here if not installed


_servo = None


class FireController:

    def __init__(self,
                 channel="P0",
                 shots_per_salvo=5,
                 salvo_count=2):

        global _servo

        print("[FIRE] initializing hardware...")

        _servo = Servo(channel)

        print("[FIRE] hardware READY")

        self.shots_per_salvo = shots_per_salvo
        self.salvo_count     = salvo_count

        # Servo angles
        self.cock_angle = 32
        self.fire_angle = 90
        self.rest_angle = 90

        # Timings (seconds)
        self.cock_time   = 1.0
        self.fire_time   = 0.25
        self.rest_time   = 0.5
        self.salvo_break = 1.0

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------

    def _set_angle(self, angle):
        if _servo is None:
            raise RuntimeError("[FIRE] servo not initialized — cannot set angle")
        _servo.angle(angle)

    def _single_shot(self):
        self._set_angle(self.cock_angle)
        time.sleep(self.cock_time)
        self._set_angle(self.fire_angle)
        time.sleep(self.fire_time)

    # --------------------------------------------------
    # PUBLIC
    # --------------------------------------------------

    def fire(self):
        print("[FIRE] SEQUENCE START")

        for s in range(self.salvo_count):
            print(f"[FIRE] salvo {s + 1} of {self.salvo_count}")

            for i in range(self.shots_per_salvo):
                print(f"[FIRE]   shot {i + 1}")
                self._single_shot()

            if s < self.salvo_count - 1:
                print(f"[FIRE] salvo break ({self.salvo_break}s)")
                time.sleep(self.salvo_break)

        # Return servo to safe rest position
        self._set_angle(self.rest_angle)
        time.sleep(self.rest_time)

        print("[FIRE] SEQUENCE COMPLETE")

    def cleanup(self):
        global _servo

        # Return to rest before releasing
        if _servo is not None:
            try:
                _servo.angle(self.rest_angle)
                time.sleep(0.3)
            except:
                pass

        _servo = None
        print("[FIRE] cleanup done")
