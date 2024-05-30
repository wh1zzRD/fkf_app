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

// REPLACE WITH YOUR RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x80, 0x7D, 0x3A, 0xF0, 0x8B, 0x88};

byte receivedData[8];

const int ledPin = 32; // LED connected to digital pin 32

// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
  int left;
  int right;
  bool light;
  bool water;
} struct_message;

// Create a struct_message called myData
struct_message myData;

esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Init Serial Monitor
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

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Transmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}
 
void loop() {
   // Create an array to hold the received bytes
  if (Serial.available() >= 6) {
    // Read the 8 bytes into the array
    for (int i = 0; i < 6; i++) {
        receivedData[i] = Serial.read();
    }
  }

  int left = receivedData[1];
  if (!receivedData[0]) {
    left *= -1;
  }

  int right = receivedData[3];
  if (!receivedData[2]) {
    right *= -1;
  }

  bool light = receivedData[4];
  bool water = receivedData[5];

  myData.left = left;
  myData.right = right;
  myData.light = light;
  myData.water = water;

  // Set values to send
  // strcpy(myData.a, "THIS IS A CHAR");
  // myData.speed1 = receivedData[0];
  // myData.speed2 = receivedData[1];
  // myData.tower1 = receivedData[2];
  // myData.tower2 = receivedData[3];
  // myData.light = receivedData[4];
  // myData.water = receivedData[5];
  // myData.b = random(1,20);
  // myData.c = 1.2;
  // myData.d = false;

  if (myData.water) { // Check the value at index 6
    digitalWrite(ledPin, HIGH); // Turn the LED on
  } else {
    digitalWrite(ledPin, LOW); // Turn the LED off
  }
  
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
}
