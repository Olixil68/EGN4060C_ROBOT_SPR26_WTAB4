# =========================
# MOCK GPIO
# =========================
# Drop-in replacement for RPi.GPIO when running on a dev/laptop machine.
# Mirrors the RPi.GPIO module-level API so it can be imported as:
#
#   from SIM.mock_gpio import GPIO
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setup(pin, GPIO.OUT)
#   pwm = GPIO.PWM(pin, 50)
#
import random


class _MockGPIO:
    """Mimics the RPi.GPIO module namespace as a single importable object."""

    BCM = "BCM"
    OUT = "OUT"
    IN  = "IN"

    def __init__(self):
        self._pins = {}

    def setmode(self, mode):
        pass

    def setup(self, pin, mode):
        self._pins[pin] = 0

    def input(self, pin):
        # ~15% chance of a simulated IR trigger each poll
        return 1 if random.random() < 0.15 else 0

    def cleanup(self):
        self._pins.clear()

    # PWM inner class
    class PWM:
        def __init__(self, pin, frequency):
            self.pin       = pin
            self.frequency = frequency
            self.duty      = 0

        def start(self, duty_cycle):
            self.duty = duty_cycle
            print(f"[MOCK-PWM] pin={self.pin} started  duty={duty_cycle}%")

        def ChangeDutyCycle(self, duty_cycle):
            self.duty = duty_cycle
            print(f"[MOCK-PWM] pin={self.pin} duty -> {duty_cycle}%")

        def stop(self):
            print(f"[MOCK-PWM] pin={self.pin} stopped")


# Single instance — imported as "GPIO" by other modules
GPIO = _MockGPIO()
