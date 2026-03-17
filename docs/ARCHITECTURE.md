# System Architecture

## Complete Pipeline

```
┌─────────────────────┐
│ Electronic Nose     │
│ (MOX/QCM Sensors)   │
│ - 8 sensors         │
│ - 100 Hz sampling   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Preprocessing       │
│ - Filtering         │
│ - Normalization     │
│ - Baseline removal  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Feature Extraction  │
│ - PCA               │
│ - Spectrogram       │
│ - Temporal stats    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Classifier Model    │
│ - CNN 1D            │
│ - Transformer       │
│ - ResNet 1D         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Diagnosis           │
│ - Probability       │
│ - Confidence        │
│ - Explainability    │
└─────────────────────┘
```

## Main Components

### 1. Data Acquisition

Electrochemical sensors (MOX/QCM) detect volatile organic compounds (VOCs) in:
- Breath
- Sweat
- Urine

Each sensor responds to different molecules:
- Acetone (diabetes)
- Benzene (cancer)
- Ammonia (renal insufficiency)
- Specific compounds (Parkinson's)

### 2. Preprocessing

**Signal filtering:**
- Low-pass filter (Butterworth) to remove high-frequency noise
- Median filter to remove baseline drift
- Gaussian smoothing

**Normalization:**
- Z-score normalization for each sensor
- Standardization across samples

### 3. Feature Extraction

**Time domain:**
- Mean, standard deviation
- Maximum, minimum, median
- Skewness, kurtosis
- RMS, peak-to-peak

**Frequency domain:**
- FFT (Fast Fourier Transform)
- Dominant frequency
- Spectral energy
- Spectral centroid

**Dimensionality reduction:**
- PCA (Principal Component Analysis)
- Spectrograms for CNNs

### 4. Classification Models

#### CNN 1D
- 1D convolutions over temporal signals
- Pooling to reduce dimensionality
- Fully connected layers for classification
- Dropout for regularization

#### Transformer
- Self-attention over temporal sequences
- Positional encoding
- Multi-head attention
- Ideal for capturing long dependencies

#### ResNet 1D
- Residual connections
- Avoids vanishing gradient
- Better for deep networks
- Global average pooling

### 5. System Output

**Prediction:**
- Predicted class (disease or healthy)
- Probability per class
- Confidence level

**Metrics:**
- Accuracy
- Precision, Recall, F1-score
- Confusion matrix
- ROC-AUC

## Data Flow

```python
# 1. Sensor reading
sensor_data = read_sensors(n_sensors=8, duration=10s)
# Shape: (8, 1000)

# 2. Preprocessing
preprocessor = SensorPreprocessor()
clean_data = preprocessor.process_sensor_array(sensor_data)
# Shape: (8, 1000)

# 3. Feature extraction (optional)
extractor = FeatureExtractor()
features = extractor.extract_all_features(clean_data)
# Shape: (96,) - 12 features × 8 sensors

# 4. Model
model = CNN1DClassifier(n_sensors=8, n_classes=2)
prediction = model(torch.tensor(clean_data))
# Shape: (2,) - probabilities per class

# 5. Result
class_name = ["Healthy", "Diabetes"][prediction.argmax()]
confidence = prediction.max().item()
```

## Design Considerations

### Scalability
- Modular: each component is independent
- Extensible: easy to add new diseases
- Configurable: YAML configs for different cases

### Performance
- Real-time inference (<1s)
- Batch processing for training
- GPU acceleration with PyTorch

### Robustness
- Cross-validation
- Data augmentation
- Ensemble methods (future)

### Explainability
- Attention weights visualization
- Feature importance
- Grad-CAM for CNNs

## Recommended Hardware

**Sensors:**
- Bosch BME688 (gas sensor with AI)
- MQ series sensors (Arduino compatible)
- Aromyx EssenceChip

**Computing:**
- Raspberry Pi 4 (inference)
- NVIDIA Jetson Nano (edge AI)
- GPU server (training)

## Technical References

- Haick et al. (2014) - "Diagnosing lung cancer in exhaled breath using gold nanoparticles"
- Amann et al. (2014) - "The human volatilome: volatile organic compounds in breath"
- Nakhleh et al. (2017) - "Diagnosis and classification of 17 diseases from 1404 subjects via pattern analysis of exhaled molecules"
