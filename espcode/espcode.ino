#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// ===============================
// Wi-Fi
// ===============================
const char* ssid = "NARZO 70 Pro 5G";
const char* password = "qwertyuiop";

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


void setup() {

  Serial.begin(115200);

  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

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

  float distance = duration * 0.0343 / 2;

  return distance;
}


void loop() {

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("WiFi disconnected!");
    delay(5000);

    return;
  }

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float distance = readDistance();

  if (isnan(temperature) || isnan(humidity)) {

    Serial.println("DHT11 reading failed!");

    delay(5000);
    return;
  }

  Serial.println();
  Serial.println("----- Sensor Data -----");

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");


  // ===============================
  // JSON
  // ===============================

  String jsonData = "{";
  jsonData += "\"temperature\":";
  jsonData += String(temperature, 2);
  jsonData += ",";
  jsonData += "\"humidity\":";
  jsonData += String(humidity, 2);
  jsonData += ",";
  jsonData += "\"distance\":";
  jsonData += String(distance, 2);
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

  // Send every 5 seconds
  delay(5000);
}