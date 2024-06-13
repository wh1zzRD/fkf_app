#define LIGHT_INPUT_PIN 9    // Pin where the PWM signal is connected
#define WATER_INPUT_PIN 12
#define LIGHT1 8
// #define LIGHT2 33
#define WATER 32

void setup() {
  pinMode(LIGHT_INPUT_PIN, INPUT);
  pinMode(LIGHT1, OUTPUT);
  // pinMode(LIGHT2, OUTPUT);

  Serial.begin(115200);
}

void toggleLight(bool state) {
  if (state) {
    digitalWrite(LIGHT1, HIGH);
    // digitalWrite(LIGHT2, HIGH);
  } else {
    digitalWrite(LIGHT1, LOW);
    // digitalWrite(LIGHT2, LOW);
  }
}

void toggleWater(bool state) {
  if (state) digitalWrite(WATER, HIGH);
  else digitalWrite(WATER, LOW);
}

void loop() {
  unsigned long highTime = pulseIn(LIGHT_INPUT_PIN, HIGH);
  unsigned long lowTime = pulseIn(LIGHT_INPUT_PIN, LOW);

  if (highTime == 0 || lowTime == 0) {
    // Avoid division by zero
    return;
  }

  // Calculate the duty cycle
  float dutyCycle = (float)highTime / (highTime + lowTime) * 100;

  Serial.print("Duty Cycle: ");
  Serial.print(dutyCycle);
  Serial.println("%");

  // Set a threshold to determine high or low output
  if (dutyCycle > 7) {
    toggleLight(1);
  } else {
    toggleLight(0);
  }

  unsigned long waterHighTime = pulseIn(WATER_INPUT_PIN, HIGH);
  unsigned long waterLowTime = pulseIn(WATER_INPUT_PIN, LOW);

  if (waterHighTime == 0 || waterLowTime == 0) {
    // Avoid division by zero
    return;
  }

  float dutyCycle2 = (float)waterHighTime / (waterHighTime + waterLowTime) * 100;
  if (dutyCycle2 > 7) {
    toggleWater(1);
  } else {
    toggleWater(0);
  }

  delay(100);  // Small delay to avoid flooding the Serial Monitor
}
