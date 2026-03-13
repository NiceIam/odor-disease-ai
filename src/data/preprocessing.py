"""
Preprocesamiento de señales de sensores electroquímicos
"""
import numpy as np
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from sklearn.preprocessing import StandardScaler


class SensorPreprocessor:
    """Preprocesa datos de sensores MOX/QCM"""
    
    def __init__(self, sampling_rate=100):
        self.sampling_rate = sampling_rate
        self.scaler = StandardScaler()
        
    def remove_baseline_drift(self, data, window_size=50):
        """Elimina deriva de línea base usando filtro de mediana"""
        baseline = signal.medfilt(data, kernel_size=window_size)
        return data - baseline
    
    def apply_lowpass_filter(self, data, cutoff_freq=10):
        """Filtro pasa-bajos para eliminar ruido de alta frecuencia"""
        nyquist = self.sampling_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, data)
    
    def smooth_signal(self, data, sigma=2):
        """Suavizado gaussiano"""
        return gaussian_filter1d(data, sigma=sigma)
    
    def normalize(self, data):
        """Normalización Z-score"""
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        return self.scaler.fit_transform(data).flatten()
    
    def process_sensor_array(self, sensor_data):
        """
        Procesa array completo de sensores
        
        Args:
            sensor_data: numpy array (n_sensors, n_samples)
        
        Returns:
            Datos procesados (n_sensors, n_samples)
        """
        processed = []
        for sensor_signal in sensor_data:
            # Pipeline de preprocesamiento
            signal_clean = self.remove_baseline_drift(sensor_signal)
            signal_filtered = self.apply_lowpass_filter(signal_clean)
            signal_smooth = self.smooth_signal(signal_filtered)
            signal_norm = self.normalize(signal_smooth)
            processed.append(signal_norm)
        
        return np.array(processed)
