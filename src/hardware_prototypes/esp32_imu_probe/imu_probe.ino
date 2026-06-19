/*
  SkyEdge ESP32 IMU Probe

  Role:
  - Prototype IMU bring-up sketch
  - Print roll, pitch, yaw-like placeholder values
  - Prepare hardware-side telemetry integration notes

  Replace mock values with actual IMU driver readings later.
*/

float mockRoll = 0.0;
float mockPitch = 0.0;
float mockYaw = 0.0;

void setup() {
  Serial.begin(115200);
  Serial.println("SkyEdge IMU probe started");
}

void loop() {
  mockRoll += 0.1;
  mockPitch += 0.05;
  mockYaw += 0.2;

  if (mockRoll > 10.0) {
    mockRoll = -10.0;
  }

  if (mockPitch > 8.0) {
    mockPitch = -8.0;
  }

  if (mockYaw > 360.0) {
    mockYaw = 0.0;
  }

  Serial.print("IMU,ROLL=");
  Serial.print(mockRoll);
  Serial.print(",PITCH=");
  Serial.print(mockPitch);
  Serial.print(",YAW=");
  Serial.println(mockYaw);

  delay(500);
}