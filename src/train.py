"""
Script de entrenamiento para modelos de clasificación
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import yaml
import argparse
from pathlib import Path
from tqdm import tqdm
import numpy as np

from data.dataset import SensorDataset
from data.preprocessing import SensorPreprocessor
from data.feature_extraction import FeatureExtractor
from models.cnn1d import CNN1DClassifier, ResCNN1D
from models.transformer import SensorTransformer


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Entrena una época"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc='Training')
    for signals, labels in pbar:
        signals, labels = signals.to(device), labels.squeeze().to(device)
        
        optimizer.zero_grad()
        outputs = model(signals)
        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({'loss': loss.item(), 'acc': 100.*correct/total})
    
    return total_loss / len(dataloader), 100. * correct / total


def validate(model, dataloader, criterion, device):
    """Valida el modelo"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for signals, labels in tqdm(dataloader, desc='Validation'):
            signals, labels = signals.to(device), labels.squeeze().to(device)
            
            outputs = model(signals)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return total_loss / len(dataloader), 100. * correct / total


def main(config_path):
    # Cargar configuración
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    # Datasets
    train_dataset = SensorDataset(config['data']['train_path'])
    val_dataset = SensorDataset(config['data']['val_path'])
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True,
        num_workers=4
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=False,
        num_workers=4
    )
    
    # Modelo
    model_type = config['model']['type']
    if model_type == 'cnn1d':
        model = CNN1DClassifier(
            n_sensors=config['model']['n_sensors'],
            signal_length=config['model']['signal_length'],
            n_classes=config['model']['n_classes']
        )
    elif model_type == 'rescnn1d':
        model = ResCNN1D(
            n_sensors=config['model']['n_sensors'],
            signal_length=config['model']['signal_length'],
            n_classes=config['model']['n_classes']
        )
    elif model_type == 'transformer':
        model = SensorTransformer(
            n_sensors=config['model']['n_sensors'],
            signal_length=config['model']['signal_length'],
            n_classes=config['model']['n_classes']
        )
    else:
        raise ValueError(f"Modelo no soportado: {model_type}")
    
    model = model.to(device)
    
    # Loss y optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['training']['learning_rate'])
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5)
    
    # Entrenamiento
    best_val_acc = 0
    checkpoint_dir = Path('checkpoints')
    checkpoint_dir.mkdir(exist_ok=True)
    
    for epoch in range(config['training']['epochs']):
        print(f'\nEpoch {epoch+1}/{config["training"]["epochs"]}')
        
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        print(f'Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%')
        print(f'Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%')
        
        scheduler.step(val_loss)
        
        # Guardar mejor modelo
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'config': config
            }, checkpoint_dir / 'best_model.pth')
            print(f'Saved best model with val_acc: {val_acc:.2f}%')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help='Path to config file')
    args = parser.parse_args()
    
    main(args.config)
