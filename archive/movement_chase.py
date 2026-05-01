import serial
from rplidar import RPLidar, RPLidarException
import time

# Ports
LIDAR_PORT = '/dev/rplidar'
ARDUINO_PORT = '/dev/arduino'
BAUD_RATE = 9600
MAX_DISTANCE = 800       # 800 mm 200- ignore objects beyond this
STOP_DISTANCE = 305       # 305 mm 75- ~1 foot (304.8mm)

def run_lidar():
    lidar = None
    arduino = None

    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        print("Arduino connected.")
        print("[ARDUINO SKIPPED] Arduino connection commented out for testing.")

        lidar = RPLidar(LIDAR_PORT, baudrate=115200)
        lidar.clean_input()
        lidar.stop()
        lidar.stop_motor()
        time.sleep(1)
        lidar.start_motor()
        time.sleep(2)
        print("LiDAR running...")

        for scan in lidar.iter_scans():
            closest_distance = float('inf')
            closest_angle = None

            for (_, angle, distance) in scan:
                if distance <= 0 or distance > MAX_DISTANCE:
                    continue

                # Exclude the back region (135°–225°)
                if 135 < angle < 225:
                    continue

                if distance < closest_distance:
                    closest_distance = distance
                    closest_angle = angle

            if closest_angle is not None:
                # Determine direction
                if closest_angle <= 45 or closest_angle >= 315:
                    direction = "FRONT"
                elif 45 < closest_angle <= 135:
                    direction = "RIGHT"
                else:  # 225–315 = LEFT
                    direction = "LEFT"

                print(f"Closest object -> Direction: {direction}, Angle: {closest_angle:.1f}°, Distance: {closest_distance:.1f} mm")

                # Determine command
                if closest_distance <= STOP_DISTANCE:
                    command = "STOP"
                else:
                    command = direction  # "FRONT", "LEFT", or "RIGHT"

                arduino.write((command + '\n').encode())
                print(f"[ARDUINO WOULD SEND]: {command}")

            else:
                print("No object detected in range.")
                arduino.write(b"STOP\n")
                print("[ARDUINO WOULD SEND]: STOP")

    except RPLidarException as e:
        print(f"LiDAR Error: {e}. Restarting...")
        if lidar:
            lidar.stop()
            lidar.disconnect()
        time.sleep(2)
        run_lidar()

    except KeyboardInterrupt:
        print("Stopped by user.")
        if arduino:
            arduino.write(b"STOP\n")
        print("[ARDUINO WOULD SEND]: STOP")

    finally:
        if lidar:
            lidar.stop()
            lidar.disconnect()
        if arduino:
            arduino.close()
        print("[ARDUINO SKIPPED] Arduino connection closed (was not open).")

run_lidar()