"""
Extracción de características de señales de sensores
"""
import numpy as np
from scipy import signal as sp_signal
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA


class FeatureExtractor:
    """Extrae características relevantes de señales de sensores"""
    
    def __init__(self, n_pca_components=10):
        self.pca = PCA(n_components=n_pca_components)
        
    def extract_statistical_features(self, signal):
        """Características estadísticas básicas"""
        features = {
            'mean': np.mean(signal),
            'std': np.std(signal),
            'max': np.max(signal),
            'min': np.min(signal),
            'median': np.median(signal),
            'skewness': skew(signal),
            'kurtosis': kurtosis(signal),
            'rms': np.sqrt(np.mean(signal**2)),
            'peak_to_peak': np.ptp(signal)
        }
        return np.array(list(features.values()))
    
    def extract_frequency_features(self, signal, sampling_rate=100):
        """Características en dominio de frecuencia"""
        # FFT
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/sampling_rate)
        
        # Magnitud del espectro
        magnitude = np.abs(fft)
        
        # Frecuencia dominante
        dominant_freq = freqs[np.argmax(magnitude[:len(magnitude)//2])]
        
        # Energía espectral
        spectral_energy = np.sum(magnitude**2)
        
        # Centroide espectral
        spectral_centroid = np.sum(freqs[:len(freqs)//2] * magnitude[:len(magnitude)//2]) / np.sum(magnitude[:len(magnitude)//2])
        
        return np.array([dominant_freq, spectral_energy, spectral_centroid])
    
    def extract_spectrogram(self, signal, sampling_rate=100, nperseg=64):
        """Genera espectrograma para CNN"""
        f, t, Sxx = sp_signal.spectrogram(signal, fs=sampling_rate, nperseg=nperseg)
        return Sxx
    
    def apply_pca(self, features_matrix):
        """Reduce dimensionalidad con PCA"""
        return self.pca.fit_transform(features_matrix)
    
    def extract_all_features(self, sensor_array):
        """
        Extrae todas las características de un array de sensores
        
        Args:
            sensor_array: numpy array (n_sensors, n_samples)
        
        Returns:
            Feature vector concatenado
        """
        all_features = []
        
        for sensor_signal in sensor_array:
            stat_features = self.extract_statistical_features(sensor_signal)
            freq_features = self.extract_frequency_features(sensor_signal)
            all_features.extend(stat_features)
            all_features.extend(freq_features)
        
        return np.array(all_features)
