void setup() {
  Serial.begin(115200);
  while (!Serial) {} //wait for serial
}

void loop() {
  while(Serial.available() > 0) {
    uint8_t c = Serial.read();
    if (c == '1') {
      Serial.println("First");
    }
    else if (c == 1) {
      Serial.println("Second");
    }
    else {
      Serial.print("Third");
      Serial.println(c);
    }
  }
}
