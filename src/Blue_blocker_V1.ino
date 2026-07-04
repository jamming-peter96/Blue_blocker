#include <SPI.h>
#include <RF24.h>

// Deine exakten nRF24-Pins (Unverändert)
#define CE1_PIN  4
#define CSN1_PIN 5
#define CE2_PIN  16
#define CSN2_PIN 17

RF24 radio1(CE1_PIN, CSN1_PIN);
RF24 radio2(CE2_PIN, CSN2_PIN);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("--- STARTE ULTRA-DOCK BLUETOOTH SENDER V1.0 ---");

  // Hardware-SPI-Bus starten (SCK=18, MISO=19, MOSI=23)
  SPI.begin(18, 19, 23, -1); 

  // Modul 1 Setup
  if (radio1.begin()) {
    radio1.setPALevel(RF24_PA_MAX);         
    radio1.setDataRate(RF24_2MBPS);         
    radio1.setAutoAck(false);               
    radio1.setCRCLength(RF24_CRC_DISABLED); // CRC aus für unstrukturiertes Rauschen
    
    // Aktiviert den rohen Sende-Modus (Constant Carrier Wave)
    radio1.startConstCarrier(RF24_PA_MAX, 2); 
    Serial.println("Modul 1: CARRIER-MODE AKTIV (Unterband)");
  } else {
    Serial.println("Modul 1: FEHLER! Verkabelung prüfen.");
  }

  // Modul 2 Setup
  if (radio2.begin()) {
    radio2.setPALevel(RF24_PA_MAX);
    radio2.setDataRate(RF24_2MBPS);
    radio2.setAutoAck(false);
    radio2.setCRCLength(RF24_CRC_DISABLED);
    
    // Aktiviert den rohen Sende-Modus (Constant Carrier Wave)
    radio2.startConstCarrier(RF24_PA_MAX, 41); 
    Serial.println("Modul 2: CARRIER-MODE AKTIV (Oberband)");
  } else {
    Serial.println("Modul 2: FEHLER! Verkabelung prüfen.");
  }

  Serial.println(">>> ROHE FUNKENERGIE AKTIVIERT <<<");
}

void loop() {
  // Synchronisiertes High-Speed Hopping (Optimiert von 10µs auf 6µs)
  // Das erhöht den Sendedurchsatz pro Sekunde massiv!
  
  // Modul 1 bearbeitet das untere Band
  for (int i = 2; i <= 40; i++) {
    radio1.setChannel(i);
    delayMicroseconds(6); 
  }
  
  // Modul 2 bearbeitet das obere Band
  for (int i = 41; i <= 80; i++) {
    radio2.setChannel(i);
    delayMicroseconds(6);
  }
}
