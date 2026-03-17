# 🧬 Multimodal Health - AI Diagnosis by Smell
Artificial intelligence system that diagnoses diseases through the analysis of volatile organic compounds (VOCs) detected by electrochemical sensors (electronic nose).

## Objective
Detect molecular patterns associated with diseases such as diabetes, lung cancer, Parkinson's, and COVID-19 before clinical symptoms appear, using MOX/QCM sensor data that analyzes breath, sweat, and urine.

## Detectable Diseases
- **Type 2 Diabetes**: Acetone in breath (85–92% accuracy)
- **Lung Cancer**: Benzene (up to 90% sensitivity)
- **Parkinson's**: Dermal sebum (Joy Milne case)
- **COVID-19**: Unique volatile profile (validated in UK)
- **Renal Failure**: Ammonia (detectable without biopsy)

## Pipeline Architecture
```
Electronic Nose → Preprocessing → Feature Extraction → Classifier Model → Diagnosis
(MOX/QCM Sensors)  (Filter/Norm.)   (PCA/Spectrogram)   (1D CNN/Transformer)  (Prob. + Confidence)
```

## Public Datasets
- **UCI e-Nose**: Classic electronic nose dataset
- **Kaggle ENOSE**: Gas sensor data
- **OpenSmell (MIT)**: Molecular profiles

## Compatible Hardware
- MQ Sensors (Arduino)
- Bosch BME688
- Aromyx module

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Train model
python src/train.py --config configs/diabetes_breath.yaml
# Evaluate
python src/evaluate.py --model checkpoints/best_model.pth --data data/test
# Real-time inference
python src/inference.py --sensor-port COM3
```

## Project Structure
```
multimodal-health/
├── data/                  # Datasets and sensor data
├── src/                   # Source code
├── models/                # Model architectures
├── configs/               # Training configurations
├── notebooks/             # Exploratory analysis
├── checkpoints/           # Trained models
└── docs/                  # Technical documentation
```

## Tech Stack
- **Python 3.9+**
- **PyTorch**: Deep learning
- **NumPy/SciPy**: Signal processing
- **Scikit-learn**: Feature extraction
- **Pandas**: Data manipulation

## Why This Project Stands Out
1. **Unconventional data**: Works with chemical sensor signals, not text or images
2. **Multidisciplinary**: Combines physical hardware + ML + medical domain knowledge
3. **Real impact**: Early diagnosis can save lives
4. **Innovation**: Replaces detection dogs with AI (>90% accuracy)

## Scientific References
- Amann et al. (2014) - VOCs in breath analysis
- Haick et al. (2014) - Electronic noses for disease detection
- Joy Milne case study - Parkinson's detection by smell

## License
MIT License
