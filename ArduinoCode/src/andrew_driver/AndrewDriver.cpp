#include "AndrewDriver.h"
#include <Arduino.h>

ADriver::ADriver(int forward_pin, int forward_channel, int backward_pin, int backward_channel) {
	this->forward_pin = forward_pin;
	this->forward_channel = forward_channel;
	this->backward_pin = backward_pin;
	this->backward_channel = backward_channel;

	ledcSetup(forward_channel, freq, resolution);
	ledcSetup(backward_channel, freq, resolution);

	ledcAttachPin(forward_pin, forward_channel);
	ledcAttachPin(backward_pin, backward_channel);
}

ADriver::set_speed(int speed) {
	if (speed == 0) {
		ledcWrite(forward_channel, 0);
		ledcWrite(backward_channel, 0);
	}
	else if (speed > 0) {
		ledcWrite(backward_channel, 0);
		ledcWrite(forward_channel, speed);
	}
	else {
		ledcWrite(forward_channel, 0);
		ledcWrite(backward_channel, speed);
	}
}