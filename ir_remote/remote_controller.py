# =========================
# REMOTE CONTROLLER (IR)
# =========================
# Reads IR sensor via lgpio on Sunfounder Robot HAT v4.
# Sensor output is digital — must go through DIGITAL port (D0).
# Wiring: VCC → 3.3V, GND → GND, OUT → D0 (GPIO17)

import lgpio
import time

GPIO_PIN = 17  # D0 on SunFounder HAT V4

class RemoteController:
    """
    Detects IR remote signal via lgpio on GPIO17 (D0).
    Call update() each loop tick; returns True once per press.
    """

    def __init__(self, pin=None, adc_channel=None):
        # pin/adc_channel kept for backwards compatibility, not used
        self.chip = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_input(self.chip, GPIO_PIN, lgpio.SET_PULL_UP)
        self.last_state = 1  # idle is HIGH (pull-up)
        print("[IR] RemoteController ready on GPIO17 (D0)")

    def update(self):
        """Returns True on falling edge (button press), False otherwise."""
        val = lgpio.gpio_read(self.chip, GPIO_PIN)
        if val == 0 and self.last_state == 1:
            self.last_state = 0
            print("[IR] START SIGNAL DETECTED")
            return True
        self.last_state = val
        return False

    def cleanup(self):
        lgpio.gpiochip_close(self.chip)
        print("[IR] GPIO released")
