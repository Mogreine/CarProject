#include <SPI.h>
#include <WiFi.h>
#include "esp_camera.h"

char ssid[] = "XXXXX";
char pass[] = "XXXXX";

int status = WL_IDLE_STATUS;
char server[] = "ipinfo.io";

WiFiClient client;

float bytes2float(uchar* bytes);
int bytes2int(uchar* bytes);
bool read_bytes(char* buffer, int size);
void printWifiStatus();
void send_img();

void setup() {
	//Initialize serial and wait for port to open:
	Serial.begin(115200);
	while (!Serial) {} //wait for serial

	Serial.print("Connecting to: ");
	Serial.println(ssid);

	while (status != WL_CONNECTED) {
		status = WiFi.begin(ssid, pass);
		delay(1000);
	}
  
	Serial.println("Connected to wifi");
	printWifiStatus();

	Serial.println("\nStarting connection to server...");
	// if you get a connection, report back via serial:
	if (client.connect(server, 80)) {
		Serial.println("connected to server");
		// Make a HTTP request:
		client.println("GET /ip HTTP/1.1");
		client.println("Host: ipinfo.io");
		client.println("Connection: close");
		client.println();
	}
}

void loop() {
	// if there are incoming bytes available
	// from the server, read them and print 
	char* r     = new char[4],
		  angle = new char[4];
	bool read_succ = true;
	read_succ |= read_bytes(r, 4);
	read_succ |= read_bytes(angle, 4);
	
	if (!read_succ) {
		Serial.println();
		Serial.println("disconnecting from server.");
		client.stop();
		
		// просто ничего не делаем
		while (true);
	}
	
	send_img();
	
	delete [] r;
	delete [] angle;
}

float bytes2float(uint8_t* bytes){
	float res;
	memcpy(&res, &bytes, sizeof(res));
	return res;
}

int bytes2int(uint8_t* bytes){
	int res;
	memcpy(&res, &bytes, sizeof(res));
	return res;
}

bool read_bytes(uint8_t* buffer, int size){
	bool succ = true;
	for (int i = 0; i < size; i++) {
		while(!client.available()) {
			if (!client.connected()) {
				return false;
			}
			delay(100);
		}
		buffer[i] = client.read();
	}
	return succ;
}

void printWifiStatus() {
	// print the SSID of the network you're attached to:
	Serial.print("SSID: ");
	Serial.println(WiFi.SSID());

	// print your WiFi shield's IP address:
	IPAddress ip = WiFi.localIP();
	Serial.print("IP Address: ");
	Serial.println(ip);

	// print the received signal strength:
	long rssi = WiFi.RSSI();
	Serial.print("signal strength (RSSI):");
	Serial.print(rssi);
	Serial.println(" dBm");
}

void send_img() {
	camera_fb_t* fb = esp_camera_fb_get();
	if (!fb) {
		Serial.println("Camera capture failed");
		return;
	}
	
	size_t jpg_buf_len = 0;	
	uint8_t* jpg_buf = NULL;
	bool jpeg_converted = frame2jpg(fb, 80, &jpg_buf, &jpg_buf_len);
	if (!jpeg_converted) {
		Serial.println("JPEG compression failed");
	}
	// Возвращаем буфер для переиспользования
	esp_camera_fb_return(fb);
	
	client.write(jpg_buf, jpg_buf_len);
}