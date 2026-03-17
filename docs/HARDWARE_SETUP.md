# Hardware Setup

## Recommended Sensors

### Option 1: MQ Sensors (Arduino)

**Advantages:**
- Affordable ($2-5 per sensor)
- Easy integration with Arduino
- Wide availability

**Disadvantages:**
- Require calibration
- Temporal drift
- Lower precision

**Sensor List:**
- MQ-2: Flammable gas, smoke
- MQ-3: Alcohol, ethanol
- MQ-4: Methane, natural gas
- MQ-5: LPG, natural gas
- MQ-6: LPG, butane
- MQ-7: Carbon monoxide
- MQ-8: Hydrogen
- MQ-135: Air quality (NH3, NOx, alcohol, benzene)

### Option 2: Bosch BME688

**Advantages:**
- Gas sensor with integrated AI
- High precision
- Temperature/humidity compensation
- 4 programmable heaters

**Disadvantages:**
- More expensive (~$15)
- Requires I2C/SPI

**Specifications:**
- Detection range: 1-500 ppm
- Interface: I2C/SPI
- Voltage: 1.7-3.6V

### Option 3: Aromyx EssenceChip

**Advantages:**
- Biosensors (real olfactory receptors)
- Maximum precision
- Biological response

**Disadvantages:**
- Very expensive ($1000+)
- Requires maintenance
- Limited lifespan

## Arduino Setup

### Required Materials

- Arduino Uno/Mega
- 8× MQ Sensors
- 8× 10kΩ Resistors
- Breadboard
- Jumper wires
- 5V power supply

### Connection Diagram

```
Arduino          MQ Sensor
-------          ---------
5V     -------> VCC
GND    -------> GND
A0     -------> AOUT (MQ-2)
A1     -------> AOUT (MQ-3)
...
A7     -------> AOUT (MQ-135)
```

### Arduino Code

Upload the code in `arduino/sensor_reader.ino` to your Arduino:

```bash
# Using Arduino IDE
1. Open arduino/sensor_reader.ino
2. Select your board (Tools > Board)
3. Select the port (Tools > Port)
4. Click Upload
```

### Sensor Calibration

1. **Warm-up:** Leave sensors on for 24-48 hours
2. **Clean air:** Expose to clean air and record R0
3. **Adjustment:** Modify R0 values in code

```cpp
const float R0[NUM_SENSORS] = {
  10.5,  // MQ-2
  12.3,  // MQ-3
  9.8,   // MQ-4
  // ... adjust according to your measurements
};
```

## Raspberry Pi Setup

### Materials

- Raspberry Pi 4
- Bosch BME688 breakout board
- Jumper wires

### I2C Connection

```
Raspberry Pi     BME688
------------     ------
3.3V      ---->  VCC
GND       ---->  GND
SDA (GPIO 2) --> SDA
SCL (GPIO 3) --> SCL
```

### Library Installation

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install bme680
```

### Python Code

```python
import bme680
import time

sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

# Configure heater
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

while True:
    if sensor.get_sensor_data():
        print(f"Gas: {sensor.data.gas_resistance} Ohms")
        print(f"Temp: {sensor.data.temperature} C")
        print(f"Humidity: {sensor.data.humidity} %")
    time.sleep(1)
```

## Sample Collection Protocol

### For Breath

1. **Patient preparation:**
   - 8-hour fasting
   - No smoking 2 hours before
   - No perfumes/colognes

2. **Collection:**
   - Breathe normally 3 times
   - Exhale completely into Tedlar bag
   - Seal immediately

3. **Measurement:**
   - Connect bag to sensors
   - Record for 60 seconds
   - Purge system with clean air

### For Sweat

1. **Preparation:**
   - Clean skin with alcohol
   - Let dry completely

2. **Collection:**
   - Use absorbent patch
   - Leave for 30 minutes
   - Transfer to airtight vial

3. **Measurement:**
   - Heat vial to 37°C
   - Sample headspace with sensors

## Maintenance

### Sensor Cleaning

- Weekly: Exposure to clean air for 24h
- Monthly: Cleaning with isopropyl alcohol
- Every 6 months: Complete re-calibration

### Lifespan

- MQ Sensors: 2-5 years
- BME688: 5+ years
- Aromyx: 6-12 months

## Troubleshooting

### Unstable Readings

- Verify stable power supply
- Increase warm-up time
- Check connections

### Sensor Drift

- Re-calibrate R0
- Verify ambient temperature
- Replace sensor if necessary

### Signal Noise

- Add 100nF capacitor between VCC and GND
- Use shielded cables
- Keep away from electromagnetic sources

## References

- [MQ Sensor Datasheet](https://www.pololu.com/file/0J309/MQ2.pdf)
- [BME688 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf)
- [Arduino Sensor Tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples)
