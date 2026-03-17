"""
Tests para módulo de preprocesamiento
"""
import numpy as np
import sys
sys.path.append('../src')

from data.preprocessing import SensorPreprocessor


def test_baseline_removal():
    """Test de eliminación de línea base"""
    preprocessor = SensorPreprocessor()
    
    # Señal con deriva
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * t) + 0.1 * t  # Señal + deriva lineal
    
    cleaned = preprocessor.remove_baseline_drift(signal)
    
    # La deriva debería estar reducida
    assert np.mean(cleaned) < np.mean(signal)
    print("✓ Test baseline removal passed")


def test_lowpass_filter():
    """Test de filtro pasa-bajos"""
    preprocessor = SensorPreprocessor(sampling_rate=100)
    
    # Señal con ruido de alta frecuencia
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)
    
    filtered = preprocessor.apply_lowpass_filter(signal, cutoff_freq=5)
    
    # El ruido de alta frecuencia debería estar reducido
    assert np.std(filtered) < np.std(signal)
    print("✓ Test lowpass filter passed")


def test_normalization():
    """Test de normalización"""
    preprocessor = SensorPreprocessor()
    
    signal = np.random.randn(1000) * 10 + 50
    normalized = preprocessor.normalize(signal)
    
    # Media cercana a 0, std cercana a 1
    assert abs(np.mean(normalized)) < 0.1
    assert abs(np.std(normalized) - 1.0) < 0.1
    print("✓ Test normalization passed")


def test_process_sensor_array():
    """Test de procesamiento completo"""
    preprocessor = SensorPreprocessor()
    
    # Array de 8 sensores
    sensor_data = np.random.randn(8, 1000) * 5 + 10
    processed = preprocessor.process_sensor_array(sensor_data)
    
    assert processed.shape == sensor_data.shape
    assert processed.dtype == np.float64
    print("✓ Test process sensor array passed")


if __name__ == '__main__':
    test_baseline_removal()
    test_lowpass_filter()
    test_normalization()
    test_process_sensor_array()
    print("\n✓ All preprocessing tests passed!")
