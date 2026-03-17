# 🚀 Quick Start

## Installation in 3 Steps

### 1. Clone and Install

```bash
git clone https://github.com/NiceIam/odor-disease-ai.git
cd odor-disease-ai
pip install -r requirements.txt
```

### 2. Generate Test Data

```bash
python scripts/generate_synthetic_data.py
```

### 3. Train Model

```bash
python src/train.py --config configs/diabetes_breath.yaml
```

## Basic Usage

### Train a Model

```bash
# Diabetes detection
python src/train.py --config configs/diabetes_breath.yaml

# Lung cancer detection
python src/train.py --config configs/lung_cancer.yaml

# Parkinson detection
python src/train.py --config configs/parkinson.yaml
```

### Evaluate Model

```bash
python src/evaluate.py \
  --model checkpoints/best_model.pth \
  --data data/processed/diabetes_test.npy
```

### Real-time Inference

```bash
python src/inference.py \
  --model checkpoints/best_model.pth \
  --sensor-port COM3
```

## Project Structure

```
odor-disease-ai/
├── src/
│   ├── data/              # Data processing
│   ├── models/            # Model architectures
│   ├── train.py           # Training script
│   ├── evaluate.py        # Evaluation
│   └── inference.py       # Real-time inference
├── configs/               # YAML configurations
├── data/                  # Datasets
├── notebooks/             # Jupyter notebooks
├── tests/                 # Unit tests
└── docs/                  # Documentation
```

## Available Models

### CNN 1D (Recommended to start)
- Fast and efficient
- Good for local patterns
- ~500K parameters

### ResNet 1D
- Better accuracy
- Residual connections
- ~2M parameters

### Transformer
- State of the art
- Captures long dependencies
- ~5M parameters

## Quick Configuration

Edit `configs/diabetes_breath.yaml`:

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

## Expected Results

With synthetic data:
- Accuracy: ~90%
- Training time: 10-15 min (CPU)
- Inference: <100ms per sample

## Next Steps

1. Read the [Training Guide](docs/TRAINING_GUIDE.md)
2. Explore the [Architecture](docs/ARCHITECTURE.md)
3. Review the [Datasets](docs/DATASETS.md)
4. Experiment with the [Notebook](notebooks/exploratory_analysis.ipynb)

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

### Very low accuracy
- Verify data is normalized
- Increase number of epochs
- Try another model

## Support

- Issues: https://github.com/NiceIam/odor-disease-ai/issues
- Documentation: `docs/`
- Examples: `notebooks/`
