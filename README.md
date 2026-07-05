<p align="center">
  <img src="Blue_Blocker.png" alt="Blue Blocker Logo" width="250">
</p>

# ESP32 & Dual nRF24L01 2.4GHz Signal Tester / Jammer

This project explores the vulnerability of the 2.4GHz spectrum (commonly used by Bluetooth and Wi-Fi) against continuous carrier waves. The system utilizes an ESP32-WROOM-32E and two nRF24L01+ modules to transmit raw signals across multiple frequencies in rapid succession.

> ⚠️ **Legal Disclaimer:** This project is strictly for educational, research, and testing purposes inside a controlled environment (e.g., a Faraday cage). Operating RF jamming equipment is illegal in many jurisdictions without proper authorization. The creator assumes no liability for any misuse, interference, or damage caused by this project.

---

## 📋 Requirements & Parts List

To build this project, the following components are required:

* **Microcontroller:** 1x ESP32-WROOM-32E (or compatible ESP32 development board).
* **RF Modules:** 2x nRF24L01+ (preferably the version with an external SMA antenna connector).
* **Antennas:** 2x 2.4GHz SMA rubber duck antennas.
* **Capacitors:** 2x 100 µF electrolytic capacitors (essential for power stability).
* **Cabling:** High-quality jumper wires or a custom PCB.

---

## 🛠️ Hardware & Specifications

To ensure optimal performance and reliable frequency generation, the following hardware tweaks were implemented:

* **Power Supply Stability:** Because the nRF24L01 modules experience high current spikes at maximum output power (`RF24_PA_MAX`), a **100 µF capacitor** must be soldered directly across the VCC (3.3V) and GND pins of each module. This prevents voltage drops, signal distortion, and MCU brownouts.

---

## 📈 Testing & Empirical Limitations

The setup was evaluated against modern consumer hardware, specifically an iPhone 15 and Sony wireless headphones.

### Key Findings & Limitations:
1. **Ineffective Against Modern Bluetooth Standards:** This project is **not** capable of completely severing connections or dropping packets entirely on newer Bluetooth hardware.
2. **Audio Stuttering Only:** Testing with a *JBL Go 2* speaker and *Sony headphones* showed that the music playback does not stop. It only experiences **mild to moderate stuttering/choppiness**. Modern Adaptive Frequency Hopping (AFH) protocols mitigate the carrier interference quite effectively.
3. **Range & Orientation:**
   * A maximum effective range of **up to 10 meters** was achieved. However, this only works if the target device is moved **slowly** away from the modules.
   * Line-of-sight and height matter significantly: Elevating the transmitter modules **higher off the ground** noticeably improves the interference effect.

---

## 📌 Pin Configuration (Wiring)

The two modules run simultaneously using the ESP32's independent dual SPI buses (VSPI and HSPI). Connect them according to the following layout:

| nRF24L01 Module 1 (VSPI) | ESP32 Pin | | nRF24L01 Module 2 (HSPI) | ESP32 Pin |
| :--- | :--- | :--- | :--- | :--- |
| **VCC** | 3.3V (with Cap) | | **VCC** | 3.3V (with Cap) |
| **GND** | GND | | **GND** | GND |
| **CE** | GPIO 22 | | **CE** | GPIO 16 |
| **CSN** | GPIO 21 | | **CSN** | GPIO 15 |
| **SCK** | GPIO 18 | | **SCK** | GPIO 14 |
| **MISO** | GPIO 19 | | **MISO** | GPIO 12 |
| **MOSI** | GPIO 23 | | **MOSI** | GPIO 13 |

---

## 🔌 Hardware Pinout (v2 Only)

Ensure your hardware is wired exactly according to this scheme so the Bruce-style UI and the nRF modules function properly without any button freezes.

### 📱 SH1106 OLED Display (I2C)

| Display Pin | ESP32 GPIO |
| :--- | :--- |
| **SDA** | GPIO 21 |
| **SCL / SCK** | GPIO 22 |
| **VCC** | 3.3V / 5V |
| **GND** | GND |

### 🕹️ Navigation Buttons
*Note: All tactile switches connect directly to GND. Internal pull-ups are enabled in the source code.*

| Button | ESP32 GPIO |
| :--- | :--- |
| **UP** | GPIO 26 |
| **DOWN** | GPIO 32 |
| **SELECT** | GPIO 33 |
| **LEFT** | GPIO 25 |
| **RIGHT** | GPIO 27 |

### 📡 nRF24L01+ Transceiver Array
*All three modules share the same global hardware SPI lines and are separated via independent CE/CSN channels.*

**Shared SPI Bus:**
* **MOSI:** GPIO 23
* **MISO:** GPIO 19
* **SCK:** GPIO 18

**Module-Specific Routing:**

| Transceiver | CE Pin | CSN Pin | Default Coverage Preset |
| :--- | :--- | :--- | :--- |
| **Module 1** | GPIO 16 | GPIO 4 | Zone 1 (Channels 2 - 42) |
| **Module 2** | GPIO 15 | GPIO 2 | Zone 2 (Channels 43 - 83) |
| **Module 3** | GPIO 5 | GPIO 17 | Zone 3 (Channels 84 - 124) |

---

## 🔋 Handheld Expansion (Battery Power Options)

If you want to make your Blue_Blocker portable for testing in different rooms, you can easily upgrade it to a battery-powered handheld device. You will need a **3.7V 1500mAh LiPo battery** and a **TP4056 charging module** with protection circuit.

### Battery & Charger Wiring:

| Component / Pin | Connection Target | Description |
| :--- | :--- | :--- |
| **Battery Red (+)** | TP4056 **B+** | Connects the positive LiPo terminal to the charger. |
| **Battery Black (-)** | TP4056 **B-** | Connects the negative LiPo terminal to the charger. |
| **TP4056 OUT+** | ESP32 **VIN / 5V** | Delivers power to the ESP32 board regulator. |
| **TP4056 OUT-** | ESP32 **GND** | Shared system ground. |

> 💡 *Note: Do not connect the battery directly to the 3.3V pins of the ESP32 or nRF24 modules. The TP4056 output must go into the 5V/VIN pin of the ESP32 so the onboard voltage regulator downsteps it safely to 3.3V.*

---

## 🚀 Installation

1. Install the **RF24 library** by TMRh20 via the Arduino Library Manager or your PlatformIO environment.
2. Wire your hardware according to the pinout and battery tables above.
3. Upload the source code found in the `src/` directory to your ESP32.
4. Open the Serial Monitor at **115200 Baud** to verify startup routines.
