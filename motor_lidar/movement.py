import serial
import time
import random
from rplidar import RPLidar, RPLidarException

# =========================
# MOVEMENT CONTROLLER
# =========================
# Wraps LIDAR (RPLidar) + Arduino serial into a single class
# for use by main.py's state machine.
#
# Exposes:
#   connect()           - start LIDAR + Arduino (call once at boot)
#   disconnect()        - clean shutdown
#   scan()              - one LIDAR scan → returns (detected, distance_m, aligned)
#   send(command)       - send raw command string to Arduino
#   search_tick()       - call each loop in SEARCH: runs timed random pattern
#   approach_tick()     - call each loop in APPROACH: rotate-to-face then forward
#   escape()            - 180-degree turn then drive away (cold target rejection)
#
# Arduino commands used:
#   FRONT         - drive forward
#   ROTATE_LEFT   - rotate left in place
#   ROTATE_RIGHT  - rotate right in place
#   ROTATE_180    - spin 180 degrees (must be handled by Arduino sketch)
#   STOP          - stop all motors
# =========================

# -----------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------
LIDAR_PORT       = '/dev/rplidar'
ARDUINO_PORT     = '/dev/arduino'
BAUD_RATE        = 9600

MAX_DISTANCE_MM  = 800      # mm  - ignore objects beyond this
STOP_DISTANCE_MM = 305      # mm  - ~1 foot: stop here for thermal scan
FRONT_TOLERANCE  = 20       # degrees - within ±20° of front = aligned

SEARCH_DURATION  = 3.0      # seconds per random search move
ESCAPE_DRIVE_SEC = 2.0      # seconds to drive forward after 180° turn

MM_TO_M = 0.001             # unit conversion


class MovementController:

    def __init__(self):
        self.lidar           = None
        self.arduino         = None
        self._scan_iter      = None

        # search pattern state
        self._search_command     = None
        self._search_start_time  = None

    # ------------------------------------------------------------------
    # CONNECTION
    # ------------------------------------------------------------------
    def connect(self):
        """Initialise Arduino serial link and LIDAR motor. Call once at boot."""

        # --- Arduino ---
        self.arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)           # wait for Arduino reset after serial open
        print("[MOVEMENT] Arduino connected.")

        # --- LIDAR ---
        self.lidar = RPLidar(LIDAR_PORT, baudrate=115200)
        self.lidar.clean_input()
        time.sleep(3)           # let motor spin up fully
        print("[MOVEMENT] LiDAR running.")

        self._scan_iter = self.lidar.iter_scans()

    def disconnect(self):
        """Stop LIDAR motor and close serial. Safe to call multiple times."""
        if self.lidar:
            try:
                self.lidar.stop()
                self.lidar.stop_motor()
                time.sleep(2)
                self.lidar.disconnect()
            except Exception:
                pass
            self.lidar = None

        if self.arduino and self.arduino.is_open:
            try:
                self.send("STOP")
                time.sleep(0.1)
                self.arduino.close()
            except Exception:
                pass
            self.arduino = None

        print("[MOVEMENT] Shutdown complete.")

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------
    def _get_direction(self, angle):
        """Classify angle into FRONT, LEFT, or RIGHT zone."""
        if angle <= 45 or angle >= 315:
            return "FRONT"
        elif 45 < angle <= 135:
            return "RIGHT"
        else:
            return "LEFT"

    def _is_aligned(self, angle):
        """True when object is directly ahead within FRONT_TOLERANCE."""
        return angle <= FRONT_TOLERANCE or angle >= (360 - FRONT_TOLERANCE)

    def _get_search_command(self):
        """
        Pick a random search movement:
          1 → FRONT           (drive straight)
          2 → ROTATE_LEFT     (rotate left)
          3 → ROTATE_RIGHT    (rotate right)
        Each held for SEARCH_DURATION seconds before re-rolling.
        """
        choice = random.randint(1, 3)
        return ["FRONT", "ROTATE_LEFT", "ROTATE_RIGHT"][choice - 1]

    def _raw_scan(self):
        """Pull one frame from the LIDAR iterator. Returns list of (q, angle, dist)."""
        try:
            return next(self._scan_iter)
        except RPLidarException as e:
            print(f"[MOVEMENT] LiDAR scan error: {e}")
            return []

    def _closest_in_frame(self, raw_scan):
        """
        Find closest object in the forward arc (excludes rear 135°-225°).
        Returns (closest_angle, closest_dist_mm) or (None, inf).
        """
        closest_dist  = float('inf')
        closest_angle = None

        for (_, angle, distance) in raw_scan:
            if distance <= 0 or distance > MAX_DISTANCE_MM:
                continue
            if 135 < angle < 225:   # exclude rear arc
                continue
            if distance < closest_dist:
                closest_dist  = distance
                closest_angle = angle

        return closest_angle, closest_dist

    # ------------------------------------------------------------------
    # CORE SCAN  (used by main.py)
    # ------------------------------------------------------------------
    def scan(self):
        """
        Pull one LIDAR scan frame and return object info.

        Returns:
            (detected, distance_m, aligned)
              detected   : bool  - True if any object found in forward arc
              distance_m : float - distance in METRES (None if not detected)
              aligned    : bool  - True if object is within FRONT_TOLERANCE
        """
        raw            = self._raw_scan()
        angle, dist_mm = self._closest_in_frame(raw)

        if angle is None:
            return False, None, False

        return True, dist_mm * MM_TO_M, self._is_aligned(angle)

    # ------------------------------------------------------------------
    # SEND COMMAND
    # ------------------------------------------------------------------
    def send(self, command):
        """Send a newline-terminated command string to the Arduino."""
        if self.arduino and self.arduino.is_open:
            self.arduino.write((command + '\n').encode())
            print(f"[MOVEMENT] → {command}")

    # ------------------------------------------------------------------
    # STATE TICK HELPERS  (called from main.py each loop iteration)
    # ------------------------------------------------------------------
    def search_tick(self):
        """
        One tick of the random search pattern.
        Picks a new move every SEARCH_DURATION seconds.
        Call this every loop iteration while in SEARCH state.
        Also returns (detected, distance_m, aligned) so main.py can
        transition to APPROACH as soon as an object appears.
        """
        detected, distance_m, aligned = self.scan()

        if detected:
            # Object found - cancel search pattern
            self._search_command    = None
            self._search_start_time = None
            return detected, distance_m, aligned

        # No object - keep random search pattern running
        now = time.time()
        if (self._search_command is None or
                (now - self._search_start_time) >= SEARCH_DURATION):
            self._search_command    = self._get_search_command()
            self._search_start_time = now
            print(f"[MOVEMENT] Search move: {self._search_command}")

        self.send(self._search_command)
        return False, None, False

    def reset_search(self):
        """Reset search timer so the pattern restarts fresh on next SEARCH entry."""
        self._search_command    = None
        self._search_start_time = None

    def approach_tick(self):
        """
        Drive toward a detected object.
          - Not aligned → rotate to face it.
          - Aligned, too far → drive FRONT.
          - Aligned AND within STOP_DISTANCE → STOP.

        Call every loop iteration while in APPROACH state.

        Returns:
            (in_position, detected, distance_m, aligned)
              in_position : True when robot is stopped and ready for thermal scan
              detected    : False means object was lost (return to SEARCH)
        """
        raw            = self._raw_scan()
        angle, dist_mm = self._closest_in_frame(raw)

        if angle is None:
            # Lost the target
            self.send("STOP")
            return False, False, None, False

        aligned    = self._is_aligned(angle)
        dist_m     = dist_mm * MM_TO_M
        stop_dist_m = STOP_DISTANCE_MM * MM_TO_M

        if dist_m <= stop_dist_m and aligned:
            self.send("STOP")
            return True, True, dist_m, aligned      # in position for thermal

        if not aligned:
            direction = self._get_direction(angle)
            self.send("ROTATE_RIGHT" if direction == "RIGHT" else "ROTATE_LEFT")
        else:
            self.send("FRONT")

        return False, True, dist_m, aligned

    def escape(self):
        """
        Cold-target rejection manoeuvre (called after failed thermal scan):
          1. Spin 180 degrees (Arduino handles the timed turn).
          2. Drive forward for ESCAPE_DRIVE_SEC seconds.
          3. Stop.
        Blocks until complete. main.py transitions to SEARCH afterward.
        """
        print("[MOVEMENT] Escape: rotating 180°")
        self.send("ROTATE_180")
        time.sleep(2.0)             # tune to match Arduino's 180° turn duration

        print("[MOVEMENT] Escape: driving away")
        self.send("FRONT")
        time.sleep(ESCAPE_DRIVE_SEC)

        self.send("STOP")
        print("[MOVEMENT] Escape complete.")
