int steps = 5; // stepper
int dir=4;  //stepper direction
float t = 0; // stepper pause between steps
#include <ezButton.h>
ezButton S1(11);  // buttons for max rotation from steppers
ezButton S2(12);


void setup() {
  pinMode(4, OUTPUT); // Richtung
  pinMode(5, OUTPUT); // Step
  pinMode(6, OUTPUT); // Receive
  pinMode(7, INPUT);

  digitalWrite(6, LOW);

  pinMode(8, OUTPUT); //MS1
  pinMode(9, OUTPUT); //MS2
  pinMode(10, OUTPUT); //MS3

  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(10, LOW); //Microstepping set to 1/16

  digitalWrite(dir,HIGH); // dir im Uhrzeigersinn

  Serial.begin(9600);
}

void turn(float t) { //t = 0: no turn, t > 0: counterclockwise, t < 0: clockwise; the greater, the slower it turns, abs(t) should be greater 1

  bool s1 = S1.getState();
  bool s2 = S2.getState();

  if (t>=1 && t <= 10) {
    digitalWrite(dir, HIGH);
    if (s2 == LOW) {
      delayMicroseconds(400);
      return;
    }

  } else if (t<= -1 && t>= -10) {
    digitalWrite(dir, LOW);
    if (s1 == LOW) {
      delayMicroseconds(400);
      return;
    }
  } else {return;}

  digitalWrite(5,HIGH);
  delayMicroseconds(400*abs(t));
  digitalWrite(5,LOW);
  delayMicroseconds(400*abs(t));
}

int receive() {
  int s = map(pulseIn(7, HIGH), 1000, 2000, -255, 255);
  if (abs(s) < 20) {
    return 0;
  }
  s = 255/s;
  //Serial.println(s);
  return s;
}



void loop() {
  S1.loop(); // MUST call the loop() function first
  S2.loop(); // MUST call the loop() function first
  t = receive(); //t muss auf Receiversignal gemapped werden
  Serial.println(t);
  //t = 1;
  for (int i = 0; i <20; i++) {
  turn(t);
  }
}
