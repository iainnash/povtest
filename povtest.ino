#define SIMULATE_POV

#include "TeensyPovDisplay.h"

#define NUM_LEDS 36

extern const LedArrayStruct colorCrossStruct;

const uint8_t clockPin = 13;
const uint8_t dataPin = 11;
const uint8_t analogInPin = A0;
const uint8_t motorPin = A21;
const uint32_t numLeds = NUM_LEDS;

CRGB leds[numLeds];
TeensyPovDisplay display;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("Starting POV - Test 1");
  FastLED.addLeds<APA102, dataPin, clockPin, BGR, DATA_RATE_MHZ(24)>(leds,
      numLeds);

  TeensyPOV::povSetup(hallPin, leds, numLeds);
  display.load(&colorCrossStruct);
  display.activate();
}

void loop() {
  int windSenVal = analogRead(analogInPin);
  int adjWindVal = winSenVal - 450;
  if (adjWindVal < 0) { adjWindVal = 0; }
  adjWindVal *= 5.5;
  if (adjWindVal > 1000) { adjWindVal = 1000; }
  int fanVal = (adjWindVal / 58) + 108;
  if (fanVal > 123) { fanVal = 123; }
  if (adjWindVal > 125) {
    analogWrite(motorPin, fanVal);
  } else {
    analogWrite(motorPin, 0);
  }
  delay(500);
}
