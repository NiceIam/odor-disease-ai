"""
Script de evaluación y métricas
"""
import torch
from torch.utils.data import DataLoader
import argparse
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from data.dataset import SensorDataset
from models.cnn1d import CNN1DClassifier, ResCNN1D
from models.transformer import SensorTransformer


def evaluate_model(model, dataloader, device, class_names):
    """Evalúa el modelo y genera métricas"""
    model.eval()
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for signals, labels in dataloader:
            signals = signals.to(device)
            labels = labels.squeeze()
            
            outputs = model(signals)
            probs = torch.softmax(outputs, dim=1)
            _, predicted = outputs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())
    
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_probs = np.array(all_probs)
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, target_names=class_names))
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print("Confusion matrix saved to confusion_matrix.png")
    
    # Accuracy por clase
    accuracy_per_class = cm.diagonal() / cm.sum(axis=1)
    print("\nAccuracy per class:")
    for i, class_name in enumerate(class_names):
        print(f"{class_name}: {accuracy_per_class[i]*100:.2f}%")
    
    return all_preds, all_labels, all_probs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, help='Path to model checkpoint')
    parser.add_argument('--data', type=str, required=True, help='Path to test data')
    parser.add_argument('--batch-size', type=int, default=32)
    args = parser.parse_args()
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Cargar checkpoint
    checkpoint = torch.load(args.model, map_location=device)
    config = checkpoint['config']
    
    # Cargar modelo
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
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    
    # Dataset
    test_dataset = SensorDataset(args.data)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Nombres de clases
    class_names = config.get('class_names', [f'Class_{i}' for i in range(config['model']['n_classes'])])
    
    # Evaluar
    evaluate_model(model, test_loader, device, class_names)


if __name__ == '__main__':
    main()
