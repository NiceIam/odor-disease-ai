# Available Datasets

## Public Datasets

### 1. UCI Machine Learning Repository - Gas Sensor Array

**URL:** https://archive.ics.uci.edu/ml/datasets/gas+sensor+array+drift+dataset

**Description:**
- 13,910 measurements from 16 gas sensors
- 6 different gas classes
- Data collected over 36 months
- Includes temporal sensor drift

**Format:**
- CSV files
- Features: 128 (16 sensors × 8 features)

**Usage:**
```python
import pandas as pd
data = pd.read_csv('gas_sensor_data.csv')
```

### 2. Kaggle - Electronic Nose Dataset

**URL:** https://www.kaggle.com/datasets/

**Description:**
- Electronic nose data
- Multiple sensor types
- Applications in disease detection

### 3. OpenSmell (MIT)

**URL:** https://openbci.com/

**Description:**
- Molecular odor profiles
- Volatile compound database
- Structure-odor mapping

## Disease-Specific Medical Datasets

### Diabetes Detection

**Biomarker:** Acetone in breath

**Characteristics:**
- Acetone concentration: 1.8-3.7 ppm (diabetics) vs 0.3-0.9 ppm (healthy)
- Other VOCs: isoprene, methanol

**Reference papers:**
- Deng et al. (2004) - "Determination of acetone in human breath by gas chromatography"
- Righettoni et al. (2012) - "Breath acetone monitoring by portable Si:WO3 gas sensors"

### Lung Cancer Detection

**Biomarker:** Benzene, toluene, xylene

**Characteristics:**
- Profile of 9 distinctive VOCs
- Sensitivity: 85-90%
- Specificity: 80-85%

**Reference papers:**
- Phillips et al. (2003) - "Volatile organic compounds in breath as markers of lung cancer"
- Peng et al. (2010) - "Detection of lung, breast, colorectal, and prostate cancers from exhaled breath"

### Parkinson's Disease

**Biomarker:** Dermal sebum (Joy Milne case)

**Characteristics:**
- Hippuric acid
- Eicosane
- Octadecanal

**Reference papers:**
- Trivedi et al. (2019) - "Discovery of volatile biomarkers of Parkinson's disease from sebum"

## Data Format

### Recommended Structure

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

### NPY Format

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

### CSV Format

```csv
timestamp,sensor_1,sensor_2,sensor_3,...,sensor_8,label
0.00,1.23,2.45,1.67,...,3.21,0
0.01,1.25,2.43,1.69,...,3.19,0
...
```

## Synthetic Data Generation

For testing and development, use the included script:

```bash
python scripts/generate_synthetic_data.py
```

This generates:
- 400 training samples per class
- 100 validation samples per class
- 100 test samples per class
- 8 sensors × 1000 temporal samples

## Real Data Collection

### Required Hardware

1. **Arduino + MQ Sensors**
   - MQ-2: Flammable gas
   - MQ-3: Alcohol
   - MQ-4: Methane
   - MQ-135: Air quality

2. **Bosch BME688**
   - Gas sensor with integrated AI
   - I2C/SPI interface
   - 4 programmable heaters

3. **Collection Protocol**
   - 8-hour fasting
   - Breath sample in Tedlar bag
   - 60-second sensor exposure
   - Record metadata (age, sex, medications)

### Acquisition Code

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

## Ethical Considerations

- Informed patient consent
- Data anonymization
- HIPAA/GDPR compliance
- Ethics committee approval

## Citations and Attribution

If you use these datasets in publications, cite:

```bibtex
@article{haick2014,
  title={Diagnosing lung cancer in exhaled breath using gold nanoparticles},
  author={Haick, Hossam and others},
  journal={Nature Nanotechnology},
  year={2014}
}
```
