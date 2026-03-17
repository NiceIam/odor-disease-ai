"""
Dataset loader for sensor data
"""
import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd


class SensorDataset(Dataset):
    """Dataset for electrochemical sensor signals"""
    
    def __init__(self, data_path, transform=None, feature_extractor=None):
        """
        Args:
            data_path: Ruta al archivo CSV o NPY
            transform: Transformaciones opcionales
            feature_extractor: Extractor de características
        """
        self.transform = transform
        self.feature_extractor = feature_extractor
        
        # Load data
        if data_path.endswith('.csv'):
            df = pd.read_csv(data_path)
            self.labels = df['label'].values
            self.data = df.drop('label', axis=1).values
        elif data_path.endswith('.npy'):
            data = np.load(data_path, allow_pickle=True).item()
            self.data = data['signals']
            self.labels = data['labels']
        else:
            raise ValueError("Unsupported format. Use CSV or NPY")
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        signal = self.data[idx]
        label = self.labels[idx]
        
        # Apply feature extraction if available
        if self.feature_extractor:
            signal = self.feature_extractor.extract_all_features(signal)
        
        # Apply transformations
        if self.transform:
            signal = self.transform(signal)
        
        # Convert to tensors
        signal = torch.FloatTensor(signal)
        label = torch.LongTensor([label])
        
        return signal, label


class SpectrogramDataset(Dataset):
    """Dataset that generates spectrograms for CNNs"""
    
    def __init__(self, data_path, sampling_rate=100, nperseg=64):
        self.sampling_rate = sampling_rate
        self.nperseg = nperseg
        
        if data_path.endswith('.npy'):
            data = np.load(data_path, allow_pickle=True).item()
            self.data = data['signals']
            self.labels = data['labels']
        else:
            raise ValueError("Use NPY format for spectrograms")
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        from scipy import signal
        
        sensor_signal = self.data[idx]
        label = self.labels[idx]
        
        # Generate spectrogram for each sensor
        spectrograms = []
        for s in sensor_signal:
            f, t, Sxx = signal.spectrogram(s, fs=self.sampling_rate, nperseg=self.nperseg)
            spectrograms.append(Sxx)
        
        # Stack as channels (n_sensors, freq_bins, time_bins)
        spectrogram = np.stack(spectrograms, axis=0)
        
        return torch.FloatTensor(spectrogram), torch.LongTensor([label])
