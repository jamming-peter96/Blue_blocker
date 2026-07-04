#include <SPI.h>
#include <RF24.h>

// Exact nRF24 pin configuration
#define CE1_PIN  4
#define CSN1_PIN 5
#define CE2_PIN  16
#define CSN2_PIN 17

RF24 radio1(CE1_PIN, CSN1_PIN);
RF24 radio2(CE2_PIN, CSN2_PIN);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("--- STARTING ULTRA-DOCK BLUETOOTH TRANSMITTER V1.0 ---");

  // Initialize hardware SPI bus (SCK=18, MISO=19, MOSI=23)
  SPI.begin(18, 19, 23, -1); 

  // Module 1 Setup (Lower Band)
  if (radio1.begin()) {
    radio1.setPALevel(RF24_PA_MAX);         
    radio1.setDataRate(RF24_2MBPS);         
    radio1.setAutoAck(false);               
    radio1.setCRCLength(RF24_CRC_DISABLED); // Disable CRC for unstructured noise
    
    // Activate raw transmission mode (Constant Carrier Wave)
    radio1.startConstCarrier(RF24_PA_MAX, 2); 
    Serial.println("Module 1: CARRIER-MODE ACTIVE (Lower Band)");
  } else {
    Serial.println("Module 1: ERROR! Check wiring.");
  }

  // Module 2 Setup (Upper Band)
  if (radio2.begin()) {
    radio2.setPALevel(RF24_PA_MAX);
    radio2.setDataRate(RF24_2MBPS);
    radio2.setAutoAck(false);
    radio2.setCRCLength(RF24_CRC_DISABLED);
    
    // Activate raw transmission mode (Constant Carrier Wave)
    radio2.startConstCarrier(RF24_PA_MAX, 41); 
    Serial.println("Module 2: CARRIER-MODE ACTIVE (Upper Band)");
  } else {
    Serial.println("Module 2: ERROR! Check wiring.");
  }

  Serial.println(">>> RAW RF ENERGY ACTIVATED <<<");
}

void loop() {
  // Synchronized High-Speed Hopping (Optimized to 6µs delay)
  
  // Module 1 processes the lower band (Channels 2 to 40)
  for (int i = 2; i <= 40; i++) {
    radio1.setChannel(i);
    delayMicroseconds(6); 
  }
  
  // Module 2 processes the upper band (Channels 41 to 80)
  for (int i = 41; i <= 80; i++) {
    radio2.setChannel(i);
    delayMicroseconds(6);
  }
}
