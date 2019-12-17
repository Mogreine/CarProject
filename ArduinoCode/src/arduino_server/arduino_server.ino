#include <WiFi.h>
#include "esp_camera.h"
#include <cmath>

#define IN1 4
#define IN2 2         // IN2 обязательно должен быть ШИМ пином!!!
#define IN3 14
#define IN4 15        // IN4 обязательно должен быть ШИМ пином!!!

const double pi = 3.141;

struct CarSpeed {
  int left = 255;
  int right = 255;
  bool direction = 0;
  
//  CarSpeed(int _left, int _right, bool _direction) {
//    left = _left;
//    right = _right;
//    direction = _direction;
//  }
} CarSpeed;

void init_motor(uint8_t pin1, uint8_t pin2, uint8_t channel1, uint8_t channel2) {
  ledcSetup(channel1, 50000, 8);
  ledcAttachPin(pin1, channel1);
  
  ledcSetup(channel2, 50000, 8);
  ledcAttachPin(pin2, channel2);
}

void setSpeed(uint8_t channel1, uint8_t channel2, int wheel) {
  if (CarSpeed.direction == 1) {
    ledcWrite(channel1, wheel == 0 ? CarSpeed.left : CarSpeed.right);
    ledcWrite(channel2, 0);
  } 
  else {
    ledcWrite(channel1, 0);
    ledcWrite(channel2, wheel == 0 ? CarSpeed.left : CarSpeed.right);
  }
}

void uint2bytes(size_t num, uint8_t* buf);

const char* ssid     = "SAGEMCOM_9CB8";
const char* password = "XNVB6KEC";

WiFiServer server(9081);

void CalcSpeed(float r, float angle) {
  if (r == 0) {
    CarSpeed.direction = 0;
    CarSpeed.left = 170;
    CarSpeed.right = 170;
    return;
  }
  int curr_speed = 170 + 85 * r;
  // Going backwards
  if (angle > pi) {
    CarSpeed.direction = 0;
    angle -= pi;
  }
  else {
    CarSpeed.direction = 1;
  }
  if (angle < pi / 2) {
    CarSpeed.left = 255;
    CarSpeed.right = 170 + 85 * cos(angle);
  }
  else {
    CarSpeed.left = 170 + 85 * sin(angle);
    CarSpeed.right = 255;
  }
  char msg[20];
  sprintf(msg, "%.4f %.4f", cos(angle), sin(angle));
  Serial.println(msg);
}

void setup()
{
    Serial.begin(115200);

    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    init_motor(IN1, IN2, 2, 3);
    init_motor(IN4, IN3, 4, 5);

    setSpeed(2, 3, 0);
    setSpeed(4, 5, 1);

    server.begin();
}

int value = 0;

void loop() {
 WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                              // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                 // make a String to hold incoming data from the client
    while (client.connected() && client.connected()) {
      uint8_t* input = new uint8_t[4];
      uint8_t* input2 = new uint8_t[4];
      int read_symbols = 0;
      while(read_symbols < 4) {
        if (client.available()) {             // if there's bytes to read from the client,
          char c = client.read();             // read a byte, then
          // Serial.write(c);                    // print it out the serial monitor
          input[read_symbols] = c;
          read_symbols++;
        }  
      }
      read_symbols = 0;
      while(read_symbols < 4 && client.connected()) {
        if (client.available()) {             // if there's bytes to read from the client,
          char c = client.read();             // read a byte, then
          // Serial.write(c);                    // print it out the serial monitor
          input2[read_symbols] = c;
          read_symbols++;
        }  
      }
      float num1 = 0, num2 = 0;
      if (!client.connected()) {
        num1 = 170;
        num2 = 170;
        Serial.println("Client disconnected, speed set to minimum.");
        delete[] input;
        break;
      }
      num1 = bytes2float(input);
      num2 = bytes2float(input2);
      char num_str1[20];
      char num_str2[20];
      sprintf(num_str1, "%.4f %.4f", num1, num2);
      // sprintf(num_str2, "%.4f", num2); 
      Serial.println(num_str1);
      // Serial.println(num_str2);

      CalcSpeed(num1, num2);
      char act_speed[20];
      sprintf(act_speed, "%d %d", CarSpeed.left, CarSpeed.right);
      Serial.println(act_speed);
      setSpeed(2, 3, 0);
      setSpeed(4, 5, 1);
      
//      char* msg = "Got ur message";
//      int msg_len = strlen(msg);
//      client.write(msg, msg_len);
      delete[] input;
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}

void uint2bytes(size_t num, uint8_t* buf) {
  buf[0] = (num >> 24) & 0xFF;  
  buf[1] = (num >> 16) & 0xFF;
  buf[2] = (num >> 8) & 0xFF;
  buf[3] = num & 0xFF;  
}

float bytes2float(uint8_t* bytes){
  float res;
  memcpy(&res, bytes, sizeof(res));
  return res;
}

int bytes2int(uint8_t* bytes) {
  int res;
  memcpy(&res, bytes, sizeof(res));
  return res;
}

//bool read_bytes(uint8_t* buffer, int size){
//  bool succ = true;
// for (int i = 0; i < size; i++) {
//    while(!client.available()) {
//      if (!client.connected()) {
//        return false;
//      }
//      Serial.println("Waiting for a byte");
//      delay(100);
//    }
//    
//    buffer[i] = client.read();
//  }
//  return succ;
//}

//void send_img() {
//  camera_fb_t* fb = esp_camera_fb_get();
//  if (!fb) {
//    Serial.println("Camera capture failed");
//    return;
//  }
//  
//  size_t jpg_buf_len = 0; 
//  uint8_t* jpg_buf = NULL;
//  bool jpeg_converted = frame2jpg(fb, 80, &jpg_buf, &jpg_buf_len);
//  if (!jpeg_converted) {
//    Serial.println("JPEG compression failed");
//  }
//  // Возвращаем буфер для переиспользования
//  esp_camera_fb_return(fb);
//  
//  client.write(jpg_buf, jpg_buf_len);
//}
