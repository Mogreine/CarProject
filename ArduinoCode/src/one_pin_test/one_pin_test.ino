#include <NewPing.h>
 
#define TRIGGER_PIN  12
#define ECHO_PIN     12
#define MAX_DISTANCE 300

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
NewPing sonar2(13, 13, 300);
 
void setup() {
  Serial.begin(115200);
}
 
void loop() {
  delay(130);
  Serial.printf("Ping: %d, %d\n", sonar.ping_cm(), sonar2.ping_cm());
}
