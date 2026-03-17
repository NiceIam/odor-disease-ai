# 🚀 Inicio Rápido

## Instalación en 3 Pasos

### 1. Clonar e Instalar

```bash
git clone https://github.com/tu-usuario/salud-multimodal.git
cd salud-multimodal
pip install -r requirements.txt
```

### 2. Generar Datos de Prueba

```bash
python scripts/generate_synthetic_data.py
```

### 3. Entrenar Modelo

```bash
python src/train.py --config configs/diabetes_breath.yaml
```

## Uso Básico

### Entrenar un Modelo

```bash
# Diabetes detection
python src/train.py --config configs/diabetes_breath.yaml

# Lung cancer detection
python src/train.py --config configs/lung_cancer.yaml

# Parkinson detection
python src/train.py --config configs/parkinson.yaml
```

### Evaluar Modelo

```bash
python src/evaluate.py \
  --model checkpoints/best_model.pth \
  --data data/processed/diabetes_test.npy
```

### Inferencia en Tiempo Real

```bash
python src/inference.py \
  --model checkpoints/best_model.pth \
  --sensor-port COM3
```

## Estructura del Proyecto

```
salud-multimodal/
├── src/
│   ├── data/              # Procesamiento de datos
│   ├── models/            # Arquitecturas de modelos
│   ├── train.py           # Script de entrenamiento
│   ├── evaluate.py        # Evaluación
│   └── inference.py       # Inferencia en tiempo real
├── configs/               # Configuraciones YAML
├── data/                  # Datasets
├── notebooks/             # Jupyter notebooks
├── tests/                 # Tests unitarios
└── docs/                  # Documentación
```

## Modelos Disponibles

### CNN 1D (Recomendado para empezar)
- Rápido y eficiente
- Bueno para patrones locales
- ~500K parámetros

### ResNet 1D
- Mejor accuracy
- Conexiones residuales
- ~2M parámetros

### Transformer
- Estado del arte
- Captura dependencias largas
- ~5M parámetros

## Configuración Rápida

Edita `configs/diabetes_breath.yaml`:

```yaml
model:
  type: "cnn1d"  # cnn1d, rescnn1d, transformer
  n_sensors: 8
  n_classes: 2

training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
```

## Resultados Esperados

Con datos sintéticos:
- Accuracy: ~90%
- Training time: 10-15 min (CPU)
- Inference: <100ms por muestra

## Próximos Pasos

1. Lee la [Guía de Entrenamiento](docs/TRAINING_GUIDE.md)
2. Explora la [Arquitectura](docs/ARCHITECTURE.md)
3. Revisa los [Datasets](docs/DATASETS.md)
4. Experimenta con el [Notebook](notebooks/exploratory_analysis.ipynb)

## Troubleshooting

### Error: CUDA out of memory
```yaml
training:
  batch_size: 16  # Reduce batch size
```

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Accuracy muy baja
- Verifica que los datos estén normalizados
- Aumenta el número de épocas
- Prueba otro modelo

## Soporte

- Issues: https://github.com/tu-usuario/salud-multimodal/issues
- Documentación: `docs/`
- Ejemplos: `notebooks/`
