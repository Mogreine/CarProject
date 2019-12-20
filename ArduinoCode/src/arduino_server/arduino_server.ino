#define _USE_MATH_DEFINES
#include <WiFi.h>
#include "esp_camera.h"
#include <cmath>

#define IN1 4
#define IN2 2         // IN2 обязательно должен быть ШИМ пином!!!
#define IN3 14
#define IN4 15        // IN4 обязательно должен быть ШИМ пином!!!

void uint2bytes(size_t num, uint8_t* buf);

const char* ssid     = "SAGEMCOM_9CB8";
const char* password = "XNVB6KEC";

WiFiServer server(9081);

class Car {
private:
  int left_forward_pin;
  int left_backward_pin;
  int right_forward_pin;
  int right_backward_pin;

  int left_forward_channel;
  int left_backward_channel;
  int right_forward_channel;
  int right_backward_channel;

  void set_ledc(int channel_init, int resolution = 8, int freq = 1000) {
    // setting up left motor
    ledcSetup(channel_init, freq, resolution);
    ledcAttachPin(left_forward_pin, channel_init);
    left_forward_channel = channel_init;
    channel_init++;

    ledcSetup(channel_init, freq, resolution);
    ledcAttachPin(left_backward_pin, channel_init);
    left_backward_channel = channel_init;
    channel_init++;

    // setting up right motor
    ledcSetup(channel_init, freq, resolution);
    ledcAttachPin(right_forward_pin, channel_init);
    right_forward_channel = channel_init;
    channel_init++;

    ledcSetup(channel_init, freq, resolution);
    ledcAttachPin(right_backward_pin, channel_init);
    right_backward_channel = channel_init;
  }

  void set_left_speed(int speed) {
    ledcWrite(left_forward_channel, backwards == 0 ? speed : 0);
    ledcWrite(left_backward_channel, backwards == 1 ? speed : 0);
    left_speed = speed;
  }

  void set_right_speed(int speed) {
    ledcWrite(right_forward_channel, backwards == 0 ? speed : 0);
    ledcWrite(right_backward_channel, backwards == 1 ? speed : 0);
    right_speed = speed;
  }
public:
  int left_speed;
  int right_speed;
  bool backwards;

  Car(int _left_forward_pin, int _left_backward_pin, int _right_forward_pin, int _right_backward_pin) {
    left_forward_pin = _left_forward_pin;
    left_backward_pin = _left_backward_pin;
    right_forward_pin = _right_forward_pin;
    right_backward_pin = _right_backward_pin;

    set_ledc(2);
    backwards = 0;
    set_speed(220, 220, 0);
  }

  void set_direction(bool back) {
    backwards = back;
    set_speed(left_speed, right_speed, back);
  }

  void set_speed(int left, int right, bool back) {
    backwards = back;
    set_left_speed(left);
    set_right_speed(right);
  }

  void parse_polar_coords(double r, double angle) {
    r = min(1.0, r);
    r = max(0.0, r);
    if (r < 1e-5) {
      set_speed(0, 0, 0);
      return;
    }
    int min_speed = 50,
      max_diff = 205;
    if (angle < M_PI_2) {
      set_speed(min_speed + r * max_diff, min_speed + r * sin(angle) * max_diff, 0);
    }
    else if (angle < M_PI) {
      set_speed(min_speed + r * sin(angle) * max_diff, min_speed + r * max_diff, 0);
    }
    else if (angle < 3 * M_PI / 2) {
      set_speed(min_speed + r * abs(sin(angle)) * max_diff, min_speed + r * max_diff, 1);
    }
    else {
      set_speed(min_speed + r * max_diff, min_speed + r * abs(sin(angle)) * max_diff, 1);
    }
  }
};

Car car(IN1, IN2, IN4, IN3);

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
      if (!client.connected()) {
        Serial.println("Client disconnected, speed set to minimum.");
        car.parse_polar_coords(0, 0);
        delete[] input;
        break;
      }
      float r = bytes2float(input),
            angle = bytes2float(input2);
      char num_str1[20];
      sprintf(num_str1, "%.4f %.4f", r, angle); 
      Serial.println(num_str1);

      car.parse_polar_coords(r, angle);
      
      char act_speed[20];
      sprintf(act_speed, "%d %d", car.left_speed, car.right_speed);
      Serial.println(act_speed);
      
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
