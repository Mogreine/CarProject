#include <SimpleKalmanFilter.h>
const int potPin = 25;

// variable for storing the potentiometer value
int potValue = 0;

SimpleKalmanFilter kf = SimpleKalmanFilter(30, 30, 0.1);

void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  float x = analogRead(potPin);
  float estimated_x = kf.updateEstimate(x);
  Serial.println(estimated_x);
  delay(500);
}
