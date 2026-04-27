from robot_hat import Servo, SunfounderPWM
import time

driver = SunfounderPWM(0x14)
servo = Servo(driver, "P0")

# print("Center (0°)")
# servo.angle(0)
# time.sleep(1)

# print("Right (90°)")
# servo.angle(90)
# time.sleep(1)
print("Farther Right (90°) for 2 second (off trigger)")
servo.angle(90)
time.sleep(2)

print("Right (32°) for 1 second 10 shots")
servo.angle(32)
time.sleep(1)

print("Farther Right (90°) for 2 second (off trigger)")
servo.angle(90)
time.sleep(2)

#ONE SHOT DOES NOT WORK. INCONSISTANT
# print("Right (32°) for .2 second 1 shot")
# servo.angle(32)
# time.sleep(0.1)

# print("Farther Right (90°) for 2 second (off trigger)")
# servo.angle(90)
# time.sleep(2)

# print("Right (32°) for 0.5 seconds 4 shots")
# servo.angle(32)
# time.sleep(0.5)

# print("Farther Right (90°) for 1 second (off trigger)")
# servo.angle(90)
# time.sleep(1)

# print("Left (-90°)")
# servo.angle(-90)
# time.sleep(1)

# print("Back to center")
# servo.angle(0)

print("Done!")