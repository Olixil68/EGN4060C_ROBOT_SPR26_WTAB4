# =========================
# REMOTE CONTROLLER (IR)
# =========================
# Reads IR sensor input on a GPIO pin to start the robot.
# Falls back to mock GPIO when not running on a Raspberry Pi.

try:
    import RPi.GPIO as GPIO
except ImportError:
    from SIM.mock_gpio import GPIO


class RemoteController:
    """
    Detects a rising-edge signal on the IR sensor pin.
    Call update() each loop tick; it returns True once per press.
    """

    def __init__(self, pin=17):

        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        # track previous state for edge detection
        self.last_state = 0

    def update(self):
        """Returns True on the rising edge (button press), False otherwise."""

        signal = GPIO.input(self.pin)

        if signal == 1 and self.last_state == 0:
            self.last_state = 1
            print("[IR] START SIGNAL DETECTED")
            return True

        self.last_state = signal
        return False

    def cleanup(self):
        GPIO.cleanup()
