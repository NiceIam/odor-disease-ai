"""
Genera datos sintéticos de sensores para pruebas
"""
import numpy as np
from pathlib import Path


def generate_sensor_signal(n_samples=1000, noise_level=0.1, pattern='diabetes'):
    """
    Genera señal sintética de sensor con patrones específicos
    
    Args:
        n_samples: Número de muestras temporales
        noise_level: Nivel de ruido
        pattern: Tipo de patrón ('diabetes', 'cancer', 'healthy')
    """
    t = np.linspace(0, 10, n_samples)
    
    if pattern == 'diabetes':
        # Patrón con pico de acetona
        signal = 2.0 * np.sin(2 * np.pi * 0.5 * t) + 1.5 * np.sin(2 * np.pi * 1.2 * t)
        signal += 0.8 * np.exp(-((t - 5)**2) / 2)  # Pico gaussiano
    elif pattern == 'cancer':
        # Patrón con múltiples frecuencias (benceno)
        signal = 1.5 * np.sin(2 * np.pi * 0.8 * t) + 0.7 * np.sin(2 * np.pi * 2.0 * t)
        signal += 0.5 * np.sin(2 * np.pi * 3.5 * t)
    elif pattern == 'parkinson':
        # Patrón con deriva lenta
        signal = 1.2 * np.sin(2 * np.pi * 0.3 * t) + 0.3 * t
        signal += 0.6 * np.sin(2 * np.pi * 1.5 * t)
    else:  # healthy
        # Patrón base normal
        signal = np.sin(2 * np.pi * 0.5 * t) + 0.5 * np.sin(2 * np.pi * 1.0 * t)
    
    # Añadir ruido
    noise = np.random.normal(0, noise_level, n_samples)
    signal += noise
    
    return signal


def generate_dataset(n_samples_per_class=500, n_sensors=8, signal_length=1000):
    """
    Genera dataset completo con múltiples clases
    """
    all_signals = []
    all_labels = []
    
    patterns = ['healthy', 'diabetes']
    
    for label, pattern in enumerate(patterns):
        for _ in range(n_samples_per_class):
            # Generar señales para todos los sensores
            sensor_array = []
            for sensor_id in range(n_sensors):
                # Cada sensor tiene ligeras variaciones
                noise_level = 0.1 + sensor_id * 0.01
                signal = generate_sensor_signal(signal_length, noise_level, pattern)
                sensor_array.append(signal)
            
            all_signals.append(np.array(sensor_array))
            all_labels.append(label)
    
    return np.array(all_signals), np.array(all_labels)


def main():
    """Genera y guarda datasets sintéticos"""
    
    # Crear directorios
    data_dir = Path('data/processed')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generando dataset de diabetes...")
    
    # Train set
    train_signals, train_labels = generate_dataset(n_samples_per_class=400)
    train_data = {'signals': train_signals, 'labels': train_labels}
    np.save(data_dir / 'diabetes_train.npy', train_data)
    print(f"Train set guardado: {train_signals.shape}")
    
    # Validation set
    val_signals, val_labels = generate_dataset(n_samples_per_class=100)
    val_data = {'signals': val_signals, 'labels': val_labels}
    np.save(data_dir / 'diabetes_val.npy', val_data)
    print(f"Validation set guardado: {val_signals.shape}")
    
    # Test set
    test_signals, test_labels = generate_dataset(n_samples_per_class=100)
    test_data = {'signals': test_signals, 'labels': test_labels}
    np.save(data_dir / 'diabetes_test.npy', test_data)
    print(f"Test set guardado: {test_signals.shape}")
    
    print("\n¡Datasets sintéticos generados exitosamente!")
    print(f"Ubicación: {data_dir.absolute()}")


if __name__ == '__main__':
    main()
