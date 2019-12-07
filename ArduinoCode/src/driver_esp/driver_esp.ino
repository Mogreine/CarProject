#define MOTOR_MAX 255  // максимальный сигнал на мотор (max 255)
#define JOY_MAX 40    // рабочий ход джойстика (из приложения)

#define IN1 4
#define IN2 2         // IN2 обязательно должен быть ШИМ пином!!!
#define IN3 14
#define IN4 15        // IN4 обязательно должен быть ШИМ пином!!!

#include "GyverMotorESP.h"
GMotor motorL(IN1, IN2, 1);
GMotor motorR(IN3, IN4, 2);

int dir = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  motorR.setMode(FORWARD);
  motorL.setMode(FORWARD);
  motorR.setSpeed(170);
  motorL.setSpeed(170);
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.write(dir);
//  // Serial.flush();
//  dir ^= 1;
//  delay(3000);
}
