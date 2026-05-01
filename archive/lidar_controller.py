import serial
from rplidar import RPLidar, RPLidarException
import time
import random

# Ports
LIDAR_PORT = '/dev/rplidar'
ARDUINO_PORT = '/dev/arduino'
BAUD_RATE = 9600
MAX_DISTANCE = 800
STOP_DISTANCE = 305
FRONT_TOLERANCE = 20

# Search pattern state
search_command = None
search_start_time = None
SEARCH_DURATION = 3  # seconds per search move

def get_direction(angle):
    """Classify angle into FRONT, LEFT, or RIGHT."""
    if angle <= 45 or angle >= 315:
        return "FRONT"
    elif 45 < angle <= 135:
        return "RIGHT"
    else:  # 225-315
        return "LEFT"

def is_facing_object(angle):
    """Returns True if the object is directly in front (within tolerance)."""
    return angle <= FRONT_TOLERANCE or angle >= (360 - FRONT_TOLERANCE)

def get_search_command():
    """Pick a random search movement.
    chose random number out of 3:
    1 = forward for 3 seconds
    2 = go left and forward for 3 seconds
    3 = go right and forward for 3 seconds
    """
    choice = random.randint(1, 3)
    if choice == 1:
        return "FRONT"           # 1 = forward
    elif choice == 2:
        return "ROTATE_LEFT"     # 2 = go left and forward
    else:
        return "ROTATE_RIGHT"    # 3 = go right and forward

def run_lidar():
    global search_command, search_start_time

    while True:
        lidar = None
        arduino = None
        try:
            arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            print("Arduino connected.")

            lidar = RPLidar(LIDAR_PORT, baudrate=115200)
            lidar.clean_input()
            time.sleep(3)  # longer wait for motor to stabilize
            print("LiDAR running...")

            for scan in lidar.iter_scans():
                closest_distance = float('inf')
                closest_angle = None

                for (_, angle, distance) in scan:
                    if distance <= 0 or distance > MAX_DISTANCE:
                        continue
                    # Exclude the back region (135-225)
                    if 135 < angle < 225:
                        continue
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_angle = angle

                if closest_angle is not None:
                    # Object found - reset search state
                    search_command = None
                    search_start_time = None

                    direction = get_direction(closest_angle)
                    facing = is_facing_object(closest_angle)

                    print(f"Closest object -> Direction: {direction}, "
                          f"Angle: {closest_angle:.1f}, "
                          f"Distance: {closest_distance:.1f} mm, "
                          f"Aligned: {facing}")

                    if closest_distance <= STOP_DISTANCE and facing:
                        # Close enough AND directly in front - stop
                        command = "STOP"
                    elif not facing:
                        # Object is off to the side - rotate to face it first
                        if direction == "RIGHT":
                            command = "ROTATE_RIGHT"
                        else:
                            command = "ROTATE_LEFT"
                    else:
                        # Object is in front but not close enough - move forward
                        command = "FRONT"

                else:
                    # No object detected - chose random number out of 3
                    # 1 = forward for 3 seconds
                    # 2 = go left and forward for 3 seconds
                    # 3 = go right and forward for 3 seconds
                    now = time.time()

                    # Pick a new search move if none active or timer expired
                    if search_command is None or (now - search_start_time) >= SEARCH_DURATION:
                        search_command = get_search_command()
                        search_start_time = now
                        print(f"No object detected. Search move: {search_command}")

                    command = search_command

                arduino.write((command + '\n').encode())
                print(f"[SEND]: {command}")

        except (RPLidarException, OSError) as e:
            print(f"LiDAR Error: {e}. Restarting in 3s...")
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        finally:
            if lidar:
                try:
                    lidar.stop()
                    lidar.stop_motor()
                    time.sleep(2)
                    lidar.disconnect()
                except Exception:
                    pass
            if arduino and arduino.is_open:
                try:
                    arduino.write(b"STOP\n")
                    time.sleep(0.1)
                    arduino.close()
                except Exception:
                    pass
            print("Shutdown complete.")
            time.sleep(3)

run_lidar()