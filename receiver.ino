/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-esp32-arduino-ide/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <esp_now.h>
#include <WiFi.h>

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
  byte speed1;
  byte speed2;
  byte tower1;
  byte tower2;
  byte water;
  byte sound;
  byte light;
  byte something;
} struct_message;

// Create a struct_message called myData
struct_message myData;

const int ledPin = 32; // LED connected to digital pin 32


// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Tower 1: ");
  Serial.println(myData.tower1);
  Serial.print("Tower 2: ");
  Serial.println(myData.tower2);
  Serial.print("Speed 1: ");
  Serial.println(myData.speed1);
  Serial.print("Speed 2: ");
  Serial.println(myData.speed2);
  Serial.print("Water: ");
  Serial.println(myData.water);
  Serial.print("Sound: ");
  Serial.println(myData.sound);
  Serial.print("Light: ");
  Serial.println(myData.light);
  Serial.print("Something: ");
  Serial.println(myData.something);

  if (myData.light != 0) { // Check the value at index 6
    digitalWrite(ledPin, HIGH); // Turn the LED on
  } else {
    digitalWrite(ledPin, LOW); // Turn the LED off
  }

  // Serial.print("Char: ");
  // Serial.println(myData.a);
  // Serial.print("Int: ");
  // Serial.println(myData.b);
  // Serial.print("Float: ");
  // Serial.println(myData.c);
  // Serial.print("Bool: ");
  // Serial.println(myData.d);
  Serial.println();
}
 
void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);
  
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
  digitalWrite(ledPin, LOW);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {

}
