"""
Tests para modelos
"""
import torch
import sys
sys.path.append('../src')

from models.cnn1d import CNN1DClassifier, ResCNN1D
from models.transformer import SensorTransformer


def test_cnn1d_forward():
    """Test forward pass de CNN1D"""
    model = CNN1DClassifier(n_sensors=8, signal_length=1000, n_classes=2)
    
    # Batch de 4 muestras
    x = torch.randn(4, 8, 1000)
    output = model(x)
    
    assert output.shape == (4, 2)
    print("✓ Test CNN1D forward passed")


def test_rescnn1d_forward():
    """Test forward pass de ResCNN1D"""
    model = ResCNN1D(n_sensors=8, signal_length=1000, n_classes=2)
    
    x = torch.randn(4, 8, 1000)
    output = model(x)
    
    assert output.shape == (4, 2)
    print("✓ Test ResCNN1D forward passed")


def test_transformer_forward():
    """Test forward pass de Transformer"""
    model = SensorTransformer(
        n_sensors=8,
        signal_length=1000,
        n_classes=2,
        d_model=64,
        nhead=4,
        num_layers=2
    )
    
    x = torch.randn(4, 8, 1000)
    output = model(x)
    
    assert output.shape == (4, 2)
    print("✓ Test Transformer forward passed")


def test_model_training_step():
    """Test un paso de entrenamiento"""
    model = CNN1DClassifier(n_sensors=8, signal_length=1000, n_classes=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()
    
    # Datos de ejemplo
    x = torch.randn(4, 8, 1000)
    y = torch.randint(0, 2, (4,))
    
    # Forward
    output = model(x)
    loss = criterion(output, y)
    
    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    assert loss.item() > 0
    print("✓ Test training step passed")


if __name__ == '__main__':
    test_cnn1d_forward()
    test_rescnn1d_forward()
    test_transformer_forward()
    test_model_training_step()
    print("\n✓ All model tests passed!")
