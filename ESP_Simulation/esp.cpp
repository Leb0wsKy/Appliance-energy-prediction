#include <WiFi.h>
#include <PubSubClient.h>

// WiFi
const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";

// MQTT
const char* mqtt_server = "192.168.1.50"; // your broker
WiFiClient espClient;
PubSubClient client(espClient);

// Serial for PZEM (Hardware Serial2)
HardwareSerial PZEMSerial(2);
const int RX_PIN = 16; // PZEM TX -> ESP32 RX2
const int TX_PIN = 17; // PZEM RX <- ESP32 TX2

void setupWifi(){
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
  }
}

void reconnect(){
  while(!client.connected()){
    if(client.connect("esp32_pzem_demo")) {
      // subscribe if needed (for simulation feed)
      client.subscribe("sim/pzem");
    } else {
      delay(2000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int len){
  // optionally receive simulated readings here
}

void setup() {
  Serial.begin(115200);
  PZEMSerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // typical PZEM baud
  setupWifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  // Example: read from PZEM (pseudo). Replace with actual library calls:
  // float V = pzem.voltage();
  // float I = pzem.current();
  // float P = pzem.power();
  // float S = V * I;
  // float Q = sqrt(max(0.0, S*S - P*P));

  // For demo, here we do a fake read that you will replace:
  float V = 230.0 + (random(-50,50)/100.0);
  float I = 2.0 + (random(-20,20)/100.0);
  float P = V * I * 0.95; // fake PF = 0.95
  float S = V * I;
  float Q = sqrt(max(0.0, S*S - P*P));

  // publish JSON
  char payload[200];
  snprintf(payload, sizeof(payload),
    "{\"V\":%.2f, \"I\":%.3f, \"P\":%.2f, \"Q\":%.2f, \"S\":%.2f}",
    V, I, P, Q, S);

  client.publish("factory/pzem1", payload, true); // retained true to show state
  delay(1000);
}
