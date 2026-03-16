# Configuración de Hardware

## Sensores Recomendados

### Opción 1: Sensores MQ (Arduino)

**Ventajas:**
- Económicos ($2-5 por sensor)
- Fácil integración con Arduino
- Amplia disponibilidad

**Desventajas:**
- Requieren calibración
- Deriva temporal
- Menor precisión

**Lista de Sensores:**
- MQ-2: Gas inflamable, humo
- MQ-3: Alcohol, etanol
- MQ-4: Metano, gas natural
- MQ-5: GLP, gas natural
- MQ-6: GLP, butano
- MQ-7: Monóxido de carbono
- MQ-8: Hidrógeno
- MQ-135: Calidad del aire (NH3, NOx, alcohol, benceno)

### Opción 2: Bosch BME688

**Ventajas:**
- Sensor de gas con AI integrada
- Alta precisión
- Compensación de temperatura/humedad
- 4 heaters programables

**Desventajas:**
- Más caro (~$15)
- Requiere I2C/SPI

**Especificaciones:**
- Rango de detección: 1-500 ppm
- Interfaz: I2C/SPI
- Voltaje: 1.7-3.6V

### Opción 3: Aromyx EssenceChip

**Ventajas:**
- Biosensores (receptores olfativos reales)
- Máxima precisión
- Respuesta biológica

**Desventajas:**
- Muy caro ($1000+)
- Requiere mantenimiento
- Vida útil limitada

## Configuración con Arduino

### Materiales Necesarios

- Arduino Uno/Mega
- 8× Sensores MQ
- 8× Resistencias 10kΩ
- Breadboard
- Cables jumper
- Fuente de alimentación 5V

### Esquema de Conexión

```
Arduino          Sensor MQ
-------          ---------
5V     -------> VCC
GND    -------> GND
A0     -------> AOUT (MQ-2)
A1     -------> AOUT (MQ-3)
...
A7     -------> AOUT (MQ-135)
```

### Código Arduino

Sube el código en `arduino/sensor_reader.ino` a tu Arduino:

```bash
# Usando Arduino IDE
1. Abre arduino/sensor_reader.ino
2. Selecciona tu placa (Tools > Board)
3. Selecciona el puerto (Tools > Port)
4. Haz clic en Upload
```

### Calibración de Sensores

1. **Calentamiento:** Deja los sensores encendidos 24-48 horas
2. **Aire limpio:** Expón a aire limpio y registra R0
3. **Ajuste:** Modifica los valores R0 en el código

```cpp
const float R0[NUM_SENSORS] = {
  10.5,  // MQ-2
  12.3,  // MQ-3
  9.8,   // MQ-4
  // ... ajusta según tus mediciones
};
```

## Configuración con Raspberry Pi

### Materiales

- Raspberry Pi 4
- Bosch BME688 breakout board
- Cables jumper

### Conexión I2C

```
Raspberry Pi     BME688
------------     ------
3.3V      ---->  VCC
GND       ---->  GND
SDA (GPIO 2) --> SDA
SCL (GPIO 3) --> SCL
```

### Instalación de Librerías

```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install bme680
```

### Código Python

```python
import bme680
import time

sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

# Configurar heater
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

## Protocolo de Recolección de Muestras

### Para Aliento

1. **Preparación del paciente:**
   - Ayuno de 8 horas
   - No fumar 2 horas antes
   - No usar perfumes/colonias

2. **Recolección:**
   - Respirar normalmente 3 veces
   - Exhalar completamente en bolsa Tedlar
   - Sellar inmediatamente

3. **Medición:**
   - Conectar bolsa a sensores
   - Registrar durante 60 segundos
   - Purgar sistema con aire limpio

### Para Sudor

1. **Preparación:**
   - Limpiar piel con alcohol
   - Dejar secar completamente

2. **Recolección:**
   - Usar parche absorbente
   - Dejar 30 minutos
   - Transferir a vial hermético

3. **Medición:**
   - Calentar vial a 37°C
   - Muestrear headspace con sensores

## Mantenimiento

### Limpieza de Sensores

- Cada semana: Exposición a aire limpio 24h
- Cada mes: Limpieza con alcohol isopropílico
- Cada 6 meses: Re-calibración completa

### Vida Útil

- Sensores MQ: 2-5 años
- BME688: 5+ años
- Aromyx: 6-12 meses

## Troubleshooting

### Lecturas Inestables

- Verificar alimentación estable
- Aumentar tiempo de calentamiento
- Revisar conexiones

### Deriva de Sensores

- Re-calibrar R0
- Verificar temperatura ambiente
- Reemplazar sensor si es necesario

### Ruido en Señal

- Añadir capacitor 100nF entre VCC y GND
- Usar cables apantallados
- Alejar de fuentes electromagnéticas

## Referencias

- [MQ Sensor Datasheet](https://www.pololu.com/file/0J309/MQ2.pdf)
- [BME688 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf)
- [Arduino Sensor Tutorial](https://www.arduino.cc/en/Tutorial/BuiltInExamples)
