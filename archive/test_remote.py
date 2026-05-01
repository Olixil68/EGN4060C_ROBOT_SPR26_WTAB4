# test_remote.py
from remote_controller import RemoteController
import time

rc = RemoteController(pin=17)

print("Waiting for IR signal... point remote at sensor and press button")
print("Ctrl+C to quit\n")

try:
    while True:
        if rc.update():
            print("SUCCESS - signal received, robot would start now")
        time.sleep(0.05)  # same polling rate as main loop

except KeyboardInterrupt:
    print("\nDone")
    rc.cleanup()