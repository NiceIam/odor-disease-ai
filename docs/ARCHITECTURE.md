# Arquitectura del Sistema

## Pipeline Completo

```
┌─────────────────────┐
│ Nariz Electrónica   │
│ (Sensores MOX/QCM)  │
│ - 8 sensores        │
│ - 100 Hz sampling   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Preprocesamiento    │
│ - Filtrado          │
│ - Normalización     │
│ - Baseline removal  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Feature Extraction  │
│ - PCA               │
│ - Espectrograma     │
│ - Stats temporales  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Modelo Clasificador │
│ - CNN 1D            │
│ - Transformer       │
│ - ResNet 1D         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Diagnóstico         │
│ - Probabilidad      │
│ - Confianza         │
│ - Explicabilidad    │
└─────────────────────┘
```

## Componentes Principales

### 1. Adquisición de Datos

Los sensores electroquímicos (MOX/QCM) detectan compuestos orgánicos volátiles (COVs) en:
- Aliento
- Sudor
- Orina

Cada sensor responde a diferentes moléculas:
- Acetona (diabetes)
- Benceno (cáncer)
- Amoníaco (insuficiencia renal)
- Compuestos específicos (Parkinson)

### 2. Preprocesamiento

**Filtrado de señal:**
- Filtro pasa-bajos (Butterworth) para eliminar ruido de alta frecuencia
- Filtro de mediana para eliminar deriva de línea base
- Suavizado gaussiano

**Normalización:**
- Z-score normalization para cada sensor
- Estandarización entre muestras

### 3. Extracción de Características

**Dominio temporal:**
- Media, desviación estándar
- Máximo, mínimo, mediana
- Skewness, kurtosis
- RMS, peak-to-peak

**Dominio frecuencial:**
- FFT (Fast Fourier Transform)
- Frecuencia dominante
- Energía espectral
- Centroide espectral

**Reducción dimensional:**
- PCA (Principal Component Analysis)
- Espectrogramas para CNNs

### 4. Modelos de Clasificación

#### CNN 1D
- Convoluciones 1D sobre señales temporales
- Pooling para reducir dimensionalidad
- Capas fully connected para clasificación
- Dropout para regularización

#### Transformer
- Self-attention sobre secuencias temporales
- Codificación posicional
- Multi-head attention
- Ideal para capturar dependencias largas

#### ResNet 1D
- Conexiones residuales
- Evita vanishing gradient
- Mejor para redes profundas
- Global average pooling

### 5. Salida del Sistema

**Predicción:**
- Clase predicha (enfermedad o sano)
- Probabilidad por clase
- Nivel de confianza

**Métricas:**
- Accuracy
- Precision, Recall, F1-score
- Matriz de confusión
- ROC-AUC

## Flujo de Datos

```python
# 1. Lectura de sensores
sensor_data = read_sensors(n_sensors=8, duration=10s)
# Shape: (8, 1000)

# 2. Preprocesamiento
preprocessor = SensorPreprocessor()
clean_data = preprocessor.process_sensor_array(sensor_data)
# Shape: (8, 1000)

# 3. Feature extraction (opcional)
extractor = FeatureExtractor()
features = extractor.extract_all_features(clean_data)
# Shape: (96,) - 12 features × 8 sensors

# 4. Modelo
model = CNN1DClassifier(n_sensors=8, n_classes=2)
prediction = model(torch.tensor(clean_data))
# Shape: (2,) - probabilidades por clase

# 5. Resultado
class_name = ["Sano", "Diabetes"][prediction.argmax()]
confidence = prediction.max().item()
```

## Consideraciones de Diseño

### Escalabilidad
- Modular: cada componente es independiente
- Extensible: fácil añadir nuevas enfermedades
- Configurable: YAML configs para diferentes casos

### Performance
- Inferencia en tiempo real (<1s)
- Batch processing para entrenamiento
- GPU acceleration con PyTorch

### Robustez
- Validación cruzada
- Data augmentation
- Ensemble methods (futuro)

### Explicabilidad
- Attention weights visualization
- Feature importance
- Grad-CAM para CNNs

## Hardware Recomendado

**Sensores:**
- Bosch BME688 (gas sensor con AI)
- Sensores MQ series (Arduino compatible)
- Aromyx EssenceChip

**Computación:**
- Raspberry Pi 4 (inferencia)
- NVIDIA Jetson Nano (edge AI)
- GPU server (entrenamiento)

## Referencias Técnicas

- Haick et al. (2014) - "Diagnosing lung cancer in exhaled breath using gold nanoparticles"
- Amann et al. (2014) - "The human volatilome: volatile organic compounds in breath"
- Nakhleh et al. (2017) - "Diagnosis and classification of 17 diseases from 1404 subjects via pattern analysis of exhaled molecules"
