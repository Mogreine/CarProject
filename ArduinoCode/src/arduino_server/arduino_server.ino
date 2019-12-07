#include <WiFi.h>
#include "esp_camera.h"

void uint2bytes(size_t num, uint8_t* buf);

const char* ssid     = "SAGEMCOM_9CB8";
const char* password = "XNVB6KEC";

#define CAM_PIN_PWDN    32 //power down is not used
#define CAM_PIN_RESET   -1 //software reset will be performed
#define CAM_PIN_XCLK    0
#define CAM_PIN_SIOD    26
#define CAM_PIN_SIOC    27

#define CAM_PIN_D7      35
#define CAM_PIN_D6      34
#define CAM_PIN_D5      39
#define CAM_PIN_D4      36
#define CAM_PIN_D3      21
#define CAM_PIN_D2      19
#define CAM_PIN_D1      18
#define CAM_PIN_D0       5
#define CAM_PIN_VSYNC   25
#define CAM_PIN_HREF    23
#define CAM_PIN_PCLK    22

static camera_config_t camera_config = {
    .pin_pwdn  = CAM_PIN_PWDN,
    .pin_reset = CAM_PIN_RESET,
    .pin_xclk = CAM_PIN_XCLK,
    .pin_sscb_sda = CAM_PIN_SIOD,
    .pin_sscb_scl = CAM_PIN_SIOC,

    .pin_d7 = CAM_PIN_D7,
    .pin_d6 = CAM_PIN_D6,
    .pin_d5 = CAM_PIN_D5,
    .pin_d4 = CAM_PIN_D4,
    .pin_d3 = CAM_PIN_D3,
    .pin_d2 = CAM_PIN_D2,
    .pin_d1 = CAM_PIN_D1,
    .pin_d0 = CAM_PIN_D0,
    .pin_vsync = CAM_PIN_VSYNC,
    .pin_href = CAM_PIN_HREF,
    .pin_pclk = CAM_PIN_PCLK,

    //XCLK 20MHz or 10MHz for OV2640 double FPS (Experimental)
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,

    .pixel_format = PIXFORMAT_JPEG,//YUV422,GRAYSCALE,RGB565,JPEG
    .frame_size = FRAMESIZE_QQVGA,//QQVGA-QXGA Do not use sizes above QVGA when not JPEG

    .jpeg_quality = 13, //0-63 lower number means higher quality
    .fb_count = 1 //if more than one, i2s runs in continuous mode. Use only with JPEG
};

esp_err_t camera_init(){
    //power up the camera if PWDN pin is defined
    if(CAM_PIN_PWDN != -1){
        pinMode(CAM_PIN_PWDN, OUTPUT);
        digitalWrite(CAM_PIN_PWDN, LOW);
    }

    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera Init Failed");
        return err;
    }

    return ESP_OK;
}

esp_err_t camera_capture_send(WiFiClient* client) {
    //acquire a frame
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE(TAG, "Camera Capture Failed");
        return ESP_FAIL;
    }
//    if (!frame2jpg(fb, 10, buf, len)){
//      Serial.println("Convertation failed");
//    }
    
    uint8_t* img_len_bytes = new uint8_t[4];
    uint2bytes(fb->len, img_len_bytes);
    client->write(img_len_bytes, 4);
    client->write(fb->buf, fb->len);
    Serial.println(fb->len);
      
    //return the frame buffer back to the driver for reuse
    esp_camera_fb_return(fb);
    return ESP_OK;
}

WiFiServer server(980);

void setup()
{
    Serial.begin(115200);
    pinMode(5, OUTPUT);      // set the LED pin mode

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

    camera_init();    
    server.begin();
}

int value = 0;

void loop(){
 WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {
//      uint8_t* input = new uint8_t[4];
//      int read_symbols = 0;
//      while(read_symbols < 4) {
//        if (client.available()) {             // if there's bytes to read from the client,
//          char c = client.read();             // read a byte, then
//          // Serial.write(c);                    // print it out the serial monitor
//          input[read_symbols] = c;
//          read_symbols++;
//        }  
//      }
//      float num = bytes2float(input);
//      char num_str[20];
//      sprintf(num_str, "%.4f", num); 
//      Serial.println(num_str);
      
//      char* msg = "Got ur message";
//      int msg_len = strlen(msg);
//      client.write(msg, msg_len);
//      delete[] input;

      if (camera_capture_send(&client) != ESP_OK) {
        Serial.println("Capture failed.");
      }
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
