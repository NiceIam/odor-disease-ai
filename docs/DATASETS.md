# Datasets Disponibles

## Datasets Públicos

### 1. UCI Machine Learning Repository - Gas Sensor Array

**URL:** https://archive.ics.uci.edu/ml/datasets/gas+sensor+array+drift+dataset

**Descripción:**
- 13,910 mediciones de 16 sensores de gas
- 6 clases de gases diferentes
- Datos recolectados durante 36 meses
- Incluye drift temporal de sensores

**Formato:**
- CSV files
- Features: 128 (16 sensores × 8 características)

**Uso:**
```python
import pandas as pd
data = pd.read_csv('gas_sensor_data.csv')
```

### 2. Kaggle - Electronic Nose Dataset

**URL:** https://www.kaggle.com/datasets/

**Descripción:**
- Datos de narices electrónicas
- Múltiples tipos de sensores
- Aplicaciones en detección de enfermedades

### 3. OpenSmell (MIT)

**URL:** https://openbci.com/

**Descripción:**
- Perfiles moleculares de olores
- Base de datos de compuestos volátiles
- Mapeo estructura-olor

## Datasets Médicos Específicos

### Diabetes Detection

**Biomarcador:** Acetona en aliento

**Características:**
- Concentración de acetona: 1.8-3.7 ppm (diabéticos) vs 0.3-0.9 ppm (sanos)
- Otros COVs: isopreno, metanol

**Papers de referencia:**
- Deng et al. (2004) - "Determination of acetone in human breath by gas chromatography"
- Righettoni et al. (2012) - "Breath acetone monitoring by portable Si:WO3 gas sensors"

### Lung Cancer Detection

**Biomarcador:** Benceno, tolueno, xileno

**Características:**
- Perfil de 9 COVs distintivos
- Sensibilidad: 85-90%
- Especificidad: 80-85%

**Papers de referencia:**
- Phillips et al. (2003) - "Volatile organic compounds in breath as markers of lung cancer"
- Peng et al. (2010) - "Detection of lung, breast, colorectal, and prostate cancers from exhaled breath"

### Parkinson's Disease

**Biomarcador:** Sebo dérmico (caso Joy Milne)

**Características:**
- Ácido hipúrico
- Eicosano
- Octadecanal

**Papers de referencia:**
- Trivedi et al. (2019) - "Discovery of volatile biomarkers of Parkinson's disease from sebum"

## Formato de Datos

### Estructura Recomendada

```
data/
├── raw/
│   ├── diabetes/
│   │   ├── patient_001.csv
│   │   ├── patient_002.csv
│   │   └── ...
│   └── healthy/
│       ├── control_001.csv
│       └── ...
└── processed/
    ├── diabetes_train.npy
    ├── diabetes_val.npy
    └── diabetes_test.npy
```

### Formato NPY

```python
data = {
    'signals': np.array,  # Shape: (n_samples, n_sensors, signal_length)
    'labels': np.array,   # Shape: (n_samples,)
    'metadata': {
        'sampling_rate': 100,
        'sensor_types': ['MQ2', 'MQ3', ...],
        'patient_ids': [...],
        'timestamps': [...]
    }
}
np.save('dataset.npy', data)
```

### Formato CSV

```csv
timestamp,sensor_1,sensor_2,sensor_3,...,sensor_8,label
0.00,1.23,2.45,1.67,...,3.21,0
0.01,1.25,2.43,1.69,...,3.19,0
...
```

## Generación de Datos Sintéticos

Para pruebas y desarrollo, usa el script incluido:

```bash
python scripts/generate_synthetic_data.py
```

Esto genera:
- 400 muestras de entrenamiento por clase
- 100 muestras de validación por clase
- 100 muestras de test por clase
- 8 sensores × 1000 muestras temporales

## Recolección de Datos Reales

### Hardware Necesario

1. **Arduino + Sensores MQ**
   - MQ-2: Gas inflamable
   - MQ-3: Alcohol
   - MQ-4: Metano
   - MQ-135: Calidad del aire

2. **Bosch BME688**
   - Sensor de gas con AI integrada
   - I2C/SPI interface
   - 4 heaters programables

3. **Protocolo de Recolección**
   - Ayuno de 8 horas
   - Muestra de aliento en bolsa Tedlar
   - Exposición a sensores por 60 segundos
   - Registro de metadata (edad, sexo, medicamentos)

### Código de Adquisición

```python
import serial
import numpy as np

ser = serial.Serial('COM3', 9600)

def collect_sample(duration=10):
    data = []
    for _ in range(duration * 100):  # 100 Hz
        line = ser.readline().decode().strip()
        values = [float(x) for x in line.split(',')]
        data.append(values)
    return np.array(data)
```

## Consideraciones Éticas

- Consentimiento informado de pacientes
- Anonimización de datos
- Cumplimiento con HIPAA/GDPR
- Aprobación de comité de ética

## Citas y Atribución

Si usas estos datasets en publicaciones, cita:

```bibtex
@article{haick2014,
  title={Diagnosing lung cancer in exhaled breath using gold nanoparticles},
  author={Haick, Hossam and others},
  journal={Nature Nanotechnology},
  year={2014}
}
```
