#define MOTOR_MAX 255  // максимальный сигнал на мотор (max 255)
#define JOY_MAX 40    // рабочий ход джойстика (из приложения)

#define IN1 4
#define IN2 2         // IN2 обязательно должен быть ШИМ пином!!!
#define IN3 14
#define IN4 15        // IN4 обязательно должен быть ШИМ пином!!!

//#include "GyverMotorESP.h"
//GMotor motorL(IN1, IN2, 2);
//GMotor motorR(IN4, IN3, 4);

int dir = 0;

void init_motor(uint8_t pin1, uint8_t pin2, uint8_t channel1, uint8_t channel2) {
  ledcSetup(channel1, 50000, 8);
  ledcAttachPin(pin1, channel1);
  
  ledcSetup(channel2, 50000, 8);
  ledcAttachPin(pin2, channel2);
}

void setSpeed(uint8_t channel1, uint8_t channel2, int duty) {
  ledcWrite(channel1, duty);
  ledcWrite(channel2, 0);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  init_motor(IN1, IN2, 2, 3);
  init_motor(IN4, IN3, 4, 5);

  setSpeed(2, 3, 255);
  setSpeed(4, 5, 255);
  delay(2000);
  setSpeed(2, 3, 180);
  setSpeed(4, 5, 180);
  
//  motorR.setMode(FORWARD);
//  motorL.setMode(FORWARD);
//  motorR.setSpeed(255);
//  motorL.setSpeed(255);
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.write(dir);
//  // Serial.flush();
//  dir ^= 1;
//  delay(3000);
}
