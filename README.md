# 🧬 Salud Multimodal - IA Diagnóstico por Olor

Sistema de inteligencia artificial que diagnostica enfermedades mediante el análisis de compuestos orgánicos volátiles (COVs) detectados por sensores electroquímicos (nariz artificial).

## 🎯 Objetivo

Detectar patrones moleculares asociados a enfermedades como diabetes, cáncer de pulmón, Parkinson y COVID-19 antes de que aparezcan síntomas clínicos, utilizando datos de sensores MOX/QCM que analizan aliento, sudor y orina.

## 🔬 Enfermedades Detectables

- **Diabetes tipo 2**: Acetona en aliento (85-92% accuracy)
- **Cáncer de pulmón**: Benceno (hasta 90% sensibilidad)
- **Parkinson**: Sebo dérmico (caso Joy Milne)
- **COVID-19**: Perfil volátil único (validado en UK)
- **Insuficiencia renal**: Amoníaco (detectable sin biopsia)

## 🏗️ Arquitectura del Pipeline

```
Nariz Electrónica → Preprocesamiento → Feature Extraction → Modelo Clasificador → Diagnóstico
(Sensores MOX/QCM)  (Filtrado/Norm.)   (PCA/Espectrograma)  (CNN 1D/Transformer)  (Prob. + Confianza)
```

## 📊 Datasets Públicos

- **UCI e-Nose**: Dataset clásico de narices electrónicas
- **Kaggle ENOSE**: Datos de sensores de gas
- **OpenSmell (MIT)**: Perfiles moleculares

## 🛠️ Hardware Compatible

- Sensores MQ (Arduino)
- Bosch BME688
- Aromyx module

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 📖 Uso

```bash
# Entrenar modelo
python src/train.py --config configs/diabetes_breath.yaml

# Evaluar
python src/evaluate.py --model checkpoints/best_model.pth --data data/test

# Inferencia en tiempo real
python src/inference.py --sensor-port COM3
```

## 📁 Estructura del Proyecto

```
salud-multimodal/
├── data/                  # Datasets y datos de sensores
├── src/                   # Código fuente
├── models/                # Arquitecturas de modelos
├── configs/               # Configuraciones de entrenamiento
├── notebooks/             # Análisis exploratorio
├── checkpoints/           # Modelos entrenados
└── docs/                  # Documentación técnica
```

## 🧪 Stack Tecnológico

- **Python 3.9+**
- **PyTorch**: Deep learning
- **NumPy/SciPy**: Procesamiento de señales
- **Scikit-learn**: Feature extraction
- **Pandas**: Manipulación de datos

## 🎓 Por Qué Este Proyecto Destaca

1. **Datos no convencionales**: Trabaja con señales de sensores químicos, no texto ni imágenes
2. **Multidisciplinario**: Combina hardware físico + ML + dominio médico
3. **Impacto real**: Diagnóstico temprano puede salvar vidas
4. **Innovación**: Reemplaza perros detectores con IA (>90% precisión)

## 📚 Referencias Científicas

- Amann et al. (2014) - VOCs in breath analysis
- Haick et al. (2014) - Electronic noses for disease detection
- Joy Milne case study - Parkinson's detection by smell

## 📄 Licencia

MIT License
