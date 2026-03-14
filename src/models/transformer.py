"""
Transformer para clasificación de señales de sensores
"""
import torch
import torch.nn as nn
import math


class PositionalEncoding(nn.Module):
    """Codificación posicional para Transformer"""
    
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]


class SensorTransformer(nn.Module):
    """Transformer para clasificación de señales multimodales"""
    
    def __init__(self, n_sensors=8, signal_length=1000, n_classes=5, 
                 d_model=128, nhead=8, num_layers=4, dropout=0.1):
        super(SensorTransformer, self).__init__()
        
        # Embedding de entrada
        self.input_projection = nn.Linear(n_sensors, d_model)
        self.pos_encoder = PositionalEncoding(d_model, max_len=signal_length)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, n_classes)
        )
        
    def forward(self, x):
        # x shape: (batch, n_sensors, signal_length)
        # Transponer para tener (batch, signal_length, n_sensors)
        x = x.transpose(1, 2)
        
        # Proyectar a d_model
        x = self.input_projection(x)
        
        # Añadir codificación posicional
        x = self.pos_encoder(x)
        
        # Pasar por transformer
        x = self.transformer_encoder(x)
        
        # Global average pooling sobre la dimensión temporal
        x = x.mean(dim=1)
        
        # Clasificar
        x = self.classifier(x)
        
        return x


class MultiHeadAttentionClassifier(nn.Module):
    """Clasificador simple basado en atención multi-cabeza"""
    
    def __init__(self, n_sensors=8, signal_length=1000, n_classes=5, d_model=128, nhead=4):
        super(MultiHeadAttentionClassifier, self).__init__()
        
        self.embedding = nn.Linear(n_sensors, d_model)
        self.attention = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        self.norm = nn.LayerNorm(d_model)
        self.classifier = nn.Linear(d_model, n_classes)
        
    def forward(self, x):
        # x: (batch, n_sensors, signal_length)
        x = x.transpose(1, 2)  # (batch, signal_length, n_sensors)
        
        x = self.embedding(x)
        attn_output, _ = self.attention(x, x, x)
        x = self.norm(attn_output + x)
        
        # Pooling
        x = x.mean(dim=1)
        
        return self.classifier(x)
