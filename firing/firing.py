from robot_hat import Servo, SunfounderPWM
import time

def init(self):
    self.driver = SunfounderPWM(0x14)
    self.servo = Servo(self.driver, "P0")
# driver = SunfounderPWM(0x14)
# servo = Servo(driver, "P0")

def servo_ON(self):
    print("Right (32°) for 1 second 10 shots")
    self.servo.angle(32)
    time.sleep(1)
# print("Right (32°) for 1 second 10 shots")
# servo.angle(32)
# time.sleep(1)

def servo_OFF(self):
    print("Farther Right (90°) for 2 second (off trigger)")
    self.servo.angle(90)
    time.sleep(2)
# print("Farther Right (90°) for 2 second (off trigger)")
# servo.angle(90)
# time.sleep(2)

# print("Done!")