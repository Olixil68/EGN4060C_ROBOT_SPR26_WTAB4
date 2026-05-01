import serial
from rplidar import RPLidar, RPLidarException
import time

# Ports
#OLD LIDAR_PORT = '/dev/ttyUSB1'
LIDAR_PORT = '/dev/rplidar'

MAX_DISTANCE = 800  # mm (increased for reliability)

def run_lidar():
    lidar = None
    
    try:
        lidar = RPLidar(LIDAR_PORT, baudrate=115200)
        lidar.clean_input()

        lidar.stop()
        lidar.stop_motor()
        time.sleep(1)

        lidar.start_motor()
        time.sleep(2)

        for scan in lidar.iter_scans():

            closest_distance = float('inf')
            closest_angle = None

            for (_, angle, distance) in scan:

                if distance <= 0:
                    continue

                # Center-weighted front region: ±45°
                if angle <= 45 or angle >= 315:

                    if distance < MAX_DISTANCE:
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_angle = angle

            # Output ONE stable detection per scan
            if closest_angle is not None:

                # FRONT (center ±45° around 0°)
                if angle <= 45 or angle >= 315:
                    print("FRONT")

                # RIGHT side (45° to 135°)
                elif 45 < angle <= 135:
                    print("RIGHT")

                # LEFT side (135° to 315°)
                else:
                    print("LEFT")
                
                #print(f"CENTER OBJECT -> Angle: {closest_angle:.1f}°, Distance: {closest_distance:.1f} mm")
            else:
                print("No object in front region")

    except RPLidarException as e:
        print(f"Sync Error: {e}. Restarting...")
        if lidar:
            lidar.stop()
            lidar.disconnect()
        time.sleep(2)
        run_lidar()

    except KeyboardInterrupt:
        print("Stopped by user.")

    finally:
        if lidar:
            lidar.stop()
            lidar.disconnect()


run_lidar()