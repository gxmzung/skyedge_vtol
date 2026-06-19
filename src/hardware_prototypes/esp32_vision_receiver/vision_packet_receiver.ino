/*
  SkyEdge ESP32 Vision Packet Receiver

  Role:
  - Receive simple UDP-style vision packets from companion vision module
  - Parse target detection result
  - Print result for future mission stack integration

  This is a prototype sketch and not flight-certified code.
*/

#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "SKYEDGE_TEST_AP";
const char* password = "skyedge-test-password";

WiFiUDP udp;
const int localPort = 4210;

char packetBuffer[255];

struct VisionPacket {
  int targetDetected;
  float offsetX;
  float offsetY;
  float confidence;
};

VisionPacket parseVisionPacket(char* message) {
  VisionPacket packet;
  packet.targetDetected = 0;
  packet.offsetX = 0.0;
  packet.offsetY = 0.0;
  packet.confidence = 0.0;

  sscanf(
    message,
    "TARGET=%d,OX=%f,OY=%f,CONF=%f",
    &packet.targetDetected,
    &packet.offsetX,
    &packet.offsetY,
    &packet.confidence
  );

  return packet;
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  Serial.print("Listening UDP port: ");
  Serial.println(localPort);
}

void loop() {
  int packetSize = udp.parsePacket();

  if (packetSize) {
    int len = udp.read(packetBuffer, 254);

    if (len > 0) {
      packetBuffer[len] = '\0';
    }

    VisionPacket packet = parseVisionPacket(packetBuffer);

    Serial.print("Target: ");
    Serial.print(packet.targetDetected);
    Serial.print(" OffsetX: ");
    Serial.print(packet.offsetX);
    Serial.print(" OffsetY: ");
    Serial.print(packet.offsetY);
    Serial.print(" Confidence: ");
    Serial.println(packet.confidence);
  }
}