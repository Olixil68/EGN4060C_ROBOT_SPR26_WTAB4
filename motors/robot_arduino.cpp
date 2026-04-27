// Arduino IDE recommended due to this file should be .ino extension
 
// include <arduino.h>

// Right motor
int motorPin1 = 5;
int motorPin2 = 6;
// Left motor
int motorPin3 = 10;
int motorPin4 = 11;

/*
int main(void)
{
	init();

	initVariant();

#if defined(USBCON)
	USBDevice.attach();
#endif
	
	setup();
    
	for (;;) {
		loop();
		if (serialEventRun) serialEventRun();
	}
        
	return 0;
}
*/

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  Serial.begin(9600);
}
 
void moveForward() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
}
 
void moveBackward() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
}
 
void turnLeft() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
}
 
void turnRight() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
}
 
void stopMotors() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
}
 
void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
 
    if (command == "FRONT") {
      moveForward();
 
    } else if (command == "LEFT") {
      turnLeft();
 
    } else if (command == "RIGHT") {
      turnRight();
 
    } else if (command == "BACK") {
      moveBackward();
 
    } else if (command == "STOP") {
      stopMotors();
 
    } else if (command == "ROTATE_LEFT") {
      // Spin in place to face object on left
      turnLeft();
 
    } else if (command == "ROTATE_RIGHT") {
      // Spin in place to face object on right
      turnRight();
 
    } else if (command == "ROTATE_180") {
      // Spin in place 180 degrees then stop
      // *** TUNE THIS VALUE ***
      // Start at 800ms and adjust until the robot turns ~180 degrees.
      // Slower robot = higher value, faster robot = lower value.
      turnRight();
      delay(800);
      stopMotors();
    }
  }
}
