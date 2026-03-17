# Training Guide

## Environment Setup

### 1. Installation

```bash
# Clone repository
git clone https://github.com/NiceIam/odor-disease-ai.git
cd odor-disease-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python scripts/generate_synthetic_data.py
```

This will create:
- `data/processed/diabetes_train.npy`
- `data/processed/diabetes_val.npy`
- `data/processed/diabetes_test.npy`

## Model Configuration

Edit the configuration file in `configs/diabetes_breath.yaml`:

```yaml
model:
  type: "cnn1d"  # Options: cnn1d, rescnn1d, transformer
  n_sensors: 8
  signal_length: 1000
  n_classes: 2

training:
  batch_size: 32
  epochs: 100
  learning_rate: 0.001
```

## Training

### Basic Training

```bash
python src/train.py --config configs/diabetes_breath.yaml
```

### Monitoring with TensorBoard

```bash
# In another terminal
tensorboard --logdir=runs
```

Open http://localhost:6006 in your browser.

### Training with GPU

The code automatically detects if GPU is available:

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

To force CPU:
```bash
CUDA_VISIBLE_DEVICES="" python src/train.py --config configs/diabetes_breath.yaml
```

## Evaluation

### Evaluate Trained Model

```bash
python src/evaluate.py \
  --model checkpoints/best_model.pth \
  --data data/processed/diabetes_test.npy \
  --batch-size 32
```

This will generate:
- Classification report (precision, recall, F1)
- Confusion matrix (saved as PNG)
- Accuracy per class

### Expected Metrics

For synthetic diabetes dataset:

```
              precision    recall  f1-score   support

     Healthy       0.92      0.89      0.90       100
    Diabetes       0.90      0.93      0.91       100

    accuracy                           0.91       200
   macro avg       0.91      0.91      0.91       200
weighted avg       0.91      0.91      0.91       200
```

## Hyperparameters

### Learning Rate

Experiment with different values:

```yaml
training:
  learning_rate: 0.001  # Standard
  # learning_rate: 0.0001  # More conservative
  # learning_rate: 0.01  # More aggressive
```

### Batch Size

Adjust according to your GPU memory:

```yaml
training:
  batch_size: 32   # GPU with 8GB
  # batch_size: 16   # GPU with 4GB
  # batch_size: 64   # GPU with 16GB+
```

### Model Architecture

#### CNN 1D (Fast, efficient)
```yaml
model:
  type: "cnn1d"
```

Advantages:
- Fast training
- Fewer parameters
- Good for local patterns

#### ResNet 1D (Better accuracy)
```yaml
model:
  type: "rescnn1d"
```

Advantages:
- Residual connections
- Better for deep networks
- Avoids vanishing gradient

#### Transformer (State of the art)
```yaml
model:
  type: "transformer"
```

Advantages:
- Captures long dependencies
- Self-attention
- Better for complex sequences

Disadvantages:
- Slower
- Requires more data
- More memory

## Advanced Techniques

### Data Augmentation

Add in `src/data/augmentation.py`:

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

Train first on a large dataset, then fine-tune:

```python
# Load pre-trained model
checkpoint = torch.load('pretrained_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])

# Freeze initial layers
for param in model.conv1.parameters():
    param.requires_grad = False

# Train only last layers
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()))
```

### Ensemble Methods

Combine multiple models:

```python
models = [model1, model2, model3]

def ensemble_predict(models, input_data):
    predictions = []
    for model in models:
        pred = model(input_data)
        predictions.append(pred)
    
    # Average probabilities
    ensemble_pred = torch.stack(predictions).mean(dim=0)
    return ensemble_pred
```

## Troubleshooting

### Overfitting

Symptoms:
- High train accuracy, low val accuracy
- Validation loss increases

Solutions:
```yaml
training:
  dropout: 0.5  # Increase dropout
  weight_decay: 0.001  # Add L2 regularization
```

### Underfitting

Symptoms:
- Low train and val accuracy
- Loss doesn't decrease

Solutions:
- Increase model capacity
- Train more epochs
- Reduce regularization

### Slow Convergence

Solutions:
- Increase learning rate
- Use learning rate scheduler
- Batch normalization

### Out of Memory

Solutions:
- Reduce batch size
- Use gradient accumulation
- Smaller model

## Best Practices

1. **Always use cross-validation** for small datasets
2. **Save checkpoints** every N epochs
3. **Monitor metrics** with TensorBoard
4. **Document experiments** in a log
5. **Version your data** and models
6. **Test on real data** before deployment

## Next Steps

After training a successful model:

1. Evaluate on test data
2. Analyze errors (confusion matrix)
3. Optimize hyperparameters
4. Test on real data
5. Deploy to production (see `docs/DEPLOYMENT.md`)
