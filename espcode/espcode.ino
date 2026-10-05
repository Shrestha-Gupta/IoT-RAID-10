#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// ===============================
// Wi-Fi
// ===============================
// Replace these locally before uploading to NodeMCU.
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Flask server
const char* serverURL = "http://10.46.116.227:5000/api/data";

// ===============================
// DHT11
// ===============================
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ===============================
// HC-SR04
// ===============================
#define TRIG_PIN D5
#define ECHO_PIN D6

// ===============================
// Soil Moisture
// AO -> A0
// DO -> Not connected
// ===============================
#define SOIL_PIN A0

// ===============================
// MQ-2
// DO -> D7 through voltage divider/level shifting
// AO -> Not connected
// ===============================
#define MQ2_PIN D7

// ===============================
// PIR HC-SR501
// OUT -> D1
// ===============================
#define PIR_PIN D1

void setup() {
  Serial.begin(115200);

  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(MQ2_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);

  digitalWrite(TRIG_PIN, LOW);

  Serial.println();
  Serial.println("================================");
  Serial.println(" IoT RAID 10 - NodeMCU");
  Serial.println("================================");

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("NodeMCU IP: ");
  Serial.println(WiFi.localIP());

  // Allow PIR and MQ-2 modules to stabilize.
  delay(5000);
}

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duration == 0) {
    return -1;
  }

  return duration * 0.0343 / 2.0;
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected!");
    WiFi.reconnect();
    delay(5000);
    return;
  }

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float distance = readDistance();

  int soilMoisture = analogRead(SOIL_PIN);

  int mq2State = digitalRead(MQ2_PIN);
  bool gasDetected = (mq2State == LOW);

  int pirState = digitalRead(PIR_PIN);
  bool motionDetected = (pirState == HIGH);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT11 reading failed!");
    delay(5000);
    return;
  }

  Serial.println();
  Serial.println("----- Sensor Data -----");

  Serial.print("Temperature : ");
  Serial.print(temperature, 2);
  Serial.println(" °C");

  Serial.print("Humidity    : ");
  Serial.print(humidity, 2);
  Serial.println(" %");

  Serial.print("Distance    : ");
  Serial.print(distance, 2);
  Serial.println(" cm");

  Serial.print("Soil Moisture (raw): ");
  Serial.println(soilMoisture);

  Serial.print("MQ-2        : ");
  Serial.println(gasDetected ? "GAS DETECTED" : "NORMAL");

  Serial.print("PIR         : ");
  Serial.println(motionDetected ? "MOTION DETECTED" : "NO MOTION");

  // ===============================
  // JSON
  // ===============================
  String jsonData = "{";
  jsonData += "\"temperature\":";
  jsonData += String(temperature, 2);
  jsonData += ",\"humidity\":";
  jsonData += String(humidity, 2);
  jsonData += ",\"distance\":";
  jsonData += String(distance, 2);
  jsonData += ",\"soil_moisture\":";
  jsonData += String(soilMoisture);
  jsonData += ",\"gas_detected\":";
  jsonData += (gasDetected ? "true" : "false");
  jsonData += ",\"motion_detected\":";
  jsonData += (motionDetected ? "true" : "false");
  jsonData += "}";

  Serial.print("Sending JSON: ");
  Serial.println(jsonData);

  // ===============================
  // HTTP POST
  // ===============================
  WiFiClient client;
  HTTPClient http;

  http.begin(client, serverURL);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(jsonData);

  Serial.print("HTTP Response Code: ");
  Serial.println(httpResponseCode);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Server Response:");
    Serial.println(response);
  } else {
    Serial.println("HTTP request failed!");
  }

  http.end();

  delay(5000);
}
