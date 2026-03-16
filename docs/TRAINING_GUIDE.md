# Guía de Entrenamiento

## Preparación del Entorno

### 1. Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/salud-multimodal.git
cd salud-multimodal

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Generar Datos Sintéticos

```bash
python scripts/generate_synthetic_data.py
```

Esto creará:
- `data/processed/diabetes_train.npy`
- `data/processed/diabetes_val.npy`
- `data/processed/diabetes_test.npy`

## Configuración del Modelo

Edita el archivo de configuración en `configs/diabetes_breath.yaml`:

```yaml
model:
  type: "cnn1d"  # Opciones: cnn1d, rescnn1d, transformer
  n_sensors: 8
  signal_length: 1000
  n_classes: 2

training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
```

## Entrenamiento

### Entrenamiento Básico

```bash
python src/train.py --config configs/diabetes_breath.yaml
```

### Monitoreo con TensorBoard

```bash
# En otra terminal
tensorboard --logdir=runs
```

Abre http://localhost:6006 en tu navegador.

### Entrenamiento con GPU

El código detecta automáticamente si hay GPU disponible:

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

Para forzar CPU:
```bash
CUDA_VISIBLE_DEVICES="" python src/train.py --config configs/diabetes_breath.yaml
```

## Evaluación

### Evaluar Modelo Entrenado

```bash
python src/evaluate.py \
  --model checkpoints/best_model.pth \
  --data data/processed/diabetes_test.npy \
  --batch-size 32
```

Esto generará:
- Classification report (precision, recall, F1)
- Confusion matrix (guardada como PNG)
- Accuracy por clase

### Métricas Esperadas

Para el dataset de diabetes sintético:

```
              precision    recall  f1-score   support

        Sano       0.92      0.89      0.90       100
    Diabetes       0.90      0.93      0.91       100

    accuracy                           0.91       200
   macro avg       0.91      0.91      0.91       200
weighted avg       0.91      0.91      0.91       200
```

## Hiperparámetros

### Learning Rate

Experimenta con diferentes valores:

```yaml
training:
  learning_rate: 0.001  # Estándar
  # learning_rate: 0.0001  # Más conservador
  # learning_rate: 0.01  # Más agresivo
```

### Batch Size

Ajusta según tu memoria GPU:

```yaml
training:
  batch_size: 32   # GPU con 8GB
  # batch_size: 16   # GPU con 4GB
  # batch_size: 64   # GPU con 16GB+
```

### Arquitectura del Modelo

#### CNN 1D (Rápido, eficiente)
```yaml
model:
  type: "cnn1d"
```

Ventajas:
- Entrenamiento rápido
- Menos parámetros
- Bueno para patrones locales

#### ResNet 1D (Mejor accuracy)
```yaml
model:
  type: "rescnn1d"
```

Ventajas:
- Conexiones residuales
- Mejor para redes profundas
- Evita vanishing gradient

#### Transformer (Estado del arte)
```yaml
model:
  type: "transformer"
```

Ventajas:
- Captura dependencias largas
- Self-attention
- Mejor para secuencias complejas

Desventajas:
- Más lento
- Requiere más datos
- Más memoria

## Técnicas Avanzadas

### Data Augmentation

Añade en `src/data/augmentation.py`:

```python
def add_noise(signal, noise_level=0.05):
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise

def time_shift(signal, shift_max=50):
    shift = np.random.randint(-shift_max, shift_max)
    return np.roll(signal, shift)

def scale(signal, scale_range=(0.9, 1.1)):
    scale_factor = np.random.uniform(*scale_range)
    return signal * scale_factor
```

### Transfer Learning

Entrena primero en un dataset grande, luego fine-tune:

```python
# Cargar modelo pre-entrenado
checkpoint = torch.load('pretrained_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])

# Congelar capas iniciales
for param in model.conv1.parameters():
    param.requires_grad = False

# Entrenar solo las últimas capas
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()))
```

### Ensemble Methods

Combina múltiples modelos:

```python
models = [model1, model2, model3]

def ensemble_predict(models, input_data):
    predictions = []
    for model in models:
        pred = model(input_data)
        predictions.append(pred)
    
    # Promedio de probabilidades
    ensemble_pred = torch.stack(predictions).mean(dim=0)
    return ensemble_pred
```

## Troubleshooting

### Overfitting

Síntomas:
- Train accuracy alta, val accuracy baja
- Loss de validación aumenta

Soluciones:
```yaml
training:
  dropout: 0.5  # Aumentar dropout
  weight_decay: 0.001  # Añadir L2 regularization
```

### Underfitting

Síntomas:
- Train y val accuracy bajas
- Loss no disminuye

Soluciones:
- Aumentar capacidad del modelo
- Entrenar más épocas
- Reducir regularización

### Convergencia Lenta

Soluciones:
- Aumentar learning rate
- Usar learning rate scheduler
- Batch normalization

### Out of Memory

Soluciones:
- Reducir batch size
- Usar gradient accumulation
- Modelo más pequeño

## Mejores Prácticas

1. **Siempre usa validación cruzada** para datasets pequeños
2. **Guarda checkpoints** cada N épocas
3. **Monitorea métricas** con TensorBoard
4. **Documenta experimentos** en un log
5. **Versiona tus datos** y modelos
6. **Prueba en datos reales** antes de deployment

## Próximos Pasos

Después de entrenar un modelo exitoso:

1. Evalúa en datos de test
2. Analiza errores (confusion matrix)
3. Optimiza hiperparámetros
4. Prueba en datos reales
5. Deploy en producción (ver `docs/DEPLOYMENT.md`)
