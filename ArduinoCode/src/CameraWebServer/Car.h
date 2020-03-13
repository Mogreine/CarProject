#define _USE_MATH_DEFINES
#include <cmath>
#include <Arduino.h>

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

  void set_ledc(int channel_init, int resolution, int freq);
  void set_left_speed(int speed);
  void set_right_speed(int speed);
public:
  int left_speed;
  int right_speed;
  bool backwards;

  Car(int _left_forward_pin, int _left_backward_pin, int _right_forward_pin, int _right_backward_pin);

  void set_direction(bool back);
  void set_speed(int left, int right, bool back);
  void parse_polar_coords(double r, double angle);
  void parse_coords(double x, double y);
};