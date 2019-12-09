#include <Arduino.h>

class ADriver {
public:
	ADriver(int forward_pin, int forward_channel, int backward_pin, int backward_channel);
	set_speed(int speed);
private:
	int forward_pin, backward_pin;
	int forward_channel, backward_channel;
	const int freq = 5000, resolution = 8;
};