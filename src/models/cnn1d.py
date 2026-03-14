"""
CNN 1D para clasificación de señales de sensores
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN1DClassifier(nn.Module):
    """Red convolucional 1D para señales temporales de sensores"""
    
    def __init__(self, n_sensors=8, signal_length=1000, n_classes=5, dropout=0.5):
        super(CNN1DClassifier, self).__init__()
        
        # Convolutional blocks
        self.conv1 = nn.Conv1d(n_sensors, 64, kernel_size=7, padding=3)
        self.bn1 = nn.BatchNorm1d(64)
        self.pool1 = nn.MaxPool1d(2)
        
        self.conv2 = nn.Conv1d(64, 128, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm1d(128)
        self.pool2 = nn.MaxPool1d(2)
        
        self.conv3 = nn.Conv1d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(256)
        self.pool3 = nn.MaxPool1d(2)
        
        # Calcular tamaño después de pooling
        pooled_length = signal_length // 8
        
        # Fully connected layers
        self.fc1 = nn.Linear(256 * pooled_length, 512)
        self.dropout1 = nn.Dropout(dropout)
        self.fc2 = nn.Linear(512, 128)
        self.dropout2 = nn.Dropout(dropout)
        self.fc3 = nn.Linear(128, n_classes)
        
    def forward(self, x):
        # Conv blocks
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # FC layers
        x = F.relu(self.fc1(x))
        x = self.dropout1(x)
        x = F.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        
        return x


class ResidualBlock1D(nn.Module):
    """Bloque residual para CNN 1D"""
    
    def __init__(self, in_channels, out_channels, kernel_size=3):
        super(ResidualBlock1D, self).__init__()
        
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, padding=kernel_size//2)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, padding=kernel_size//2)
        self.bn2 = nn.BatchNorm1d(out_channels)
        
        # Shortcut connection
        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1),
                nn.BatchNorm1d(out_channels)
            )
    
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(residual)
        out = F.relu(out)
        return out


class ResCNN1D(nn.Module):
    """CNN 1D con conexiones residuales"""
    
    def __init__(self, n_sensors=8, signal_length=1000, n_classes=5):
        super(ResCNN1D, self).__init__()
        
        self.conv1 = nn.Conv1d(n_sensors, 64, kernel_size=7, padding=3)
        self.bn1 = nn.BatchNorm1d(64)
        
        self.res_block1 = ResidualBlock1D(64, 128)
        self.pool1 = nn.MaxPool1d(2)
        
        self.res_block2 = ResidualBlock1D(128, 256)
        self.pool2 = nn.MaxPool1d(2)
        
        self.res_block3 = ResidualBlock1D(256, 512)
        self.pool3 = nn.MaxPool1d(2)
        
        # Global average pooling
        self.gap = nn.AdaptiveAvgPool1d(1)
        
        # Classifier
        self.fc = nn.Linear(512, n_classes)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        
        x = self.res_block1(x)
        x = self.pool1(x)
        
        x = self.res_block2(x)
        x = self.pool2(x)
        
        x = self.res_block3(x)
        x = self.pool3(x)
        
        x = self.gap(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        return x
