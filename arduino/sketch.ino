#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define LED_PIN 13    // 使用する GPIO ピン
#define LED_COUNT 10   // LED の数
#define LED_BRIGHTNESS 200 // LED の明るさ (0-255)

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_RGB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(LED_BRIGHTNESS);
  for (int i=0; i <LED_COUNT; i++){
    pixels.setPixelColor(i, 0, 0, 255); // 初期カラーをセット (青)
  }
  pixels.show();
  Serial.begin(9600);
}

void loop() {
  static char buffer[32];
  static int values[4];
  static int bytesRead = 0;

  while (Serial.available()) {
    int c = Serial.read();
    if (c == '\n') {
      buffer[bytesRead] = 0;
      bytesRead = 0;
      parseData(buffer, values);
      setPixelColor(values);
      delay(100);
      break;
    } else {
      buffer[bytesRead++] = c;
    }
  }
}

void parseData(char* data, int* values) {
  char* p = data;
  for (int i = 0; i < 4; i++) {
    values[i] = atoi(p);
    p = strchr(p, ',');
    if (p) p++;
  }
}

void setPixelColor(int* values) {
  int ledIndex = values[0];
  int r = values[1];
  int g = values[2];
  int b = values[3];
  pixels.setPixelColor(ledIndex, pixels.Color(r, g, b));
  pixels.show();
}

