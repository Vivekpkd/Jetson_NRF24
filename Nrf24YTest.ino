
#include <nRF24L01.h>
#include <printf.h>
#include <RF24.h>
#include <RF24_config.h>

RF24 radio(9,10);
byte addresses[][6] = {"1Node","2Node"};
void setup() {
  Serial.begin(9600);
  printf_begin();
  radio.begin();
radio.openWritingPipe(addresses[0]);
}

void loop() {
  Serial.println("This is a test");
  radio.printDetails();
  delay(1000);
}
