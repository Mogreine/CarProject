#include <NewPing.h>
#include <SPID.h>

#define TRIGGER_PIN  2
#define ECHO_PIN     4
#define MAX_DISTANCE 200
 
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
SPID pid(&sonar);
 
void setup() {
  Serial.begin(115200);
  pid.req_dist = 0.1;
}
 
void loop() {
  delay(50);
  double pid_val = pid.calculate();
  
  Serial.println(pid_val);
}
