#include "Car.h"

void Car::set_ledc(int channel_init, int resolution = 8, int freq = 1000) {
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

void Car::set_left_speed(int speed) {
    ledcWrite(left_forward_channel, backwards == 0 ? speed : 0);
    ledcWrite(left_backward_channel, backwards == 1 ? speed : 0);
    left_speed = speed;
}

void Car::set_right_speed(int speed) {
    ledcWrite(right_forward_channel, backwards == 0 ? speed : 0);
    ledcWrite(right_backward_channel, backwards == 1 ? speed : 0);
    right_speed = speed;
}

Car::Car(int _left_forward_pin, int _left_backward_pin, int _right_forward_pin, int _right_backward_pin) {
    left_forward_pin = _left_forward_pin;
    left_backward_pin = _left_backward_pin;
    right_forward_pin = _right_forward_pin;
    right_backward_pin = _right_backward_pin;

    set_ledc(4);
    backwards = 0;
    set_speed(0, 0, 0);
}

void Car::set_direction(bool back) {
    backwards = back;
    set_speed(left_speed, right_speed, back);
}

void Car::set_speed(int left, int right, bool back) {
    backwards = back;
    set_left_speed(left);
    set_right_speed(right);
}

void Car::parse_polar_coords(double r, double angle) {
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

void Car::parse_coords(double x, double y) {
    // validation
    x = min(1.0, x);
    x = max(-1.0, x);
    y = min(1.0, y);
    y = max(-1.0, y);

    double r = sqrt(x * x + y * y);
    if (r < 1e-5) {
      set_speed(0, 0, 0);
      return;
    }
    int min_speed = 60,
        max_diff = 160;
	y *= 0.5;
    if (x > 0 && y > 0) {
      set_speed(min_speed + r * max_diff, min_speed + r * y * max_diff, 0);
    }
    else if (x < 0 && y > 0) {
      set_speed(min_speed + r * y * max_diff, min_speed + r * max_diff, 0);
    }
    else if (x < 0 && y < 0) {
      set_speed(min_speed + r * (-y) * max_diff, min_speed + r * max_diff, 1);
    }
    else {
      set_speed(min_speed + r * max_diff, min_speed + r * (-y) * max_diff, 1);
    }
}