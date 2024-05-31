/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-one-to-many-esp32-esp8266/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/
#include <esp_now.h>
#include <WiFi.h>

//Structure example to receive data
//Must match the sender structure
typedef struct test_struct {
  bool water;
  int left;
  int right;
} test_struct;

//Create a struct_message called myData
test_struct myData;

//callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Water: ");
  Serial.println(myData.water);
  Serial.println();
  Serial.print("Speed(left, right): ");
  Serial.print(myData.left);
  Serial.print(", ");
  Serial.print(myData.right);
  Serial.println();
  drive(myData.left, myData.right);
  digitalWrite(32, HIGH);
  delay(200);
  digitalWrite(32, LOW);
}
 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);

  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(25, OUTPUT);
  
  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);
}

void drive(int left, int right) {
  if (left > 0) {
    left = map(left, 0, 255, 127, 178);
  } else if (left == 511) {
    left = 185;
  } else if (left < 0) {
    left = map(left, -255, 0, 197, 255);
  }
  if (right > 0) {
    right = map(right, 0, 255, 127, 178);
  } else if (right == 511) {
    right = 185;
  } else if (right < 0) {
    right = map(right, -255, 0, 197, 255);
  }

  analogWrite(25, right);
  analogWrite(33, left);
}
 
void loop() {

}

  
