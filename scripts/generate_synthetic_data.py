"""
Generates synthetic sensor data for testing
"""
import numpy as np
from pathlib import Path


def generate_sensor_signal(n_samples=1000, noise_level=0.1, pattern='diabetes'):
    """
    Generates synthetic sensor signal with specific patterns
    
    Args:
        n_samples: Number of temporal samples
        noise_level: Noise level
        pattern: Pattern type ('diabetes', 'cancer', 'healthy')
    """
    t = np.linspace(0, 10, n_samples)
    
    if pattern == 'diabetes':
        # Pattern with acetone peak
        signal = 2.0 * np.sin(2 * np.pi * 0.5 * t) + 1.5 * np.sin(2 * np.pi * 1.2 * t)
        signal += 0.8 * np.exp(-((t - 5)**2) / 2)  # Gaussian peak
    elif pattern == 'cancer':
        # Pattern with multiple frequencies (benzene)
        signal = 1.5 * np.sin(2 * np.pi * 0.8 * t) + 0.7 * np.sin(2 * np.pi * 2.0 * t)
        signal += 0.5 * np.sin(2 * np.pi * 3.5 * t)
    elif pattern == 'parkinson':
        # Pattern with slow drift
        signal = 1.2 * np.sin(2 * np.pi * 0.3 * t) + 0.3 * t
        signal += 0.6 * np.sin(2 * np.pi * 1.5 * t)
    else:  # healthy
        # Normal baseline pattern
        signal = np.sin(2 * np.pi * 0.5 * t) + 0.5 * np.sin(2 * np.pi * 1.0 * t)
    
    # Add noise
    noise = np.random.normal(0, noise_level, n_samples)
    signal += noise
    
    return signal


def generate_dataset(n_samples_per_class=500, n_sensors=8, signal_length=1000):
    """
    Generates complete dataset with multiple classes
    """
    all_signals = []
    all_labels = []
    
    patterns = ['healthy', 'diabetes']
    
    for label, pattern in enumerate(patterns):
        for _ in range(n_samples_per_class):
            # Generate signals for all sensors
            sensor_array = []
            for sensor_id in range(n_sensors):
                # Each sensor has slight variations
                noise_level = 0.1 + sensor_id * 0.01
                signal = generate_sensor_signal(signal_length, noise_level, pattern)
                sensor_array.append(signal)
            
            all_signals.append(np.array(sensor_array))
            all_labels.append(label)
    
    return np.array(all_signals), np.array(all_labels)


def main():
    """Generates and saves synthetic datasets"""
    
    # Create directories
    data_dir = Path('data/processed')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating diabetes dataset...")
    
    # Train set
    train_signals, train_labels = generate_dataset(n_samples_per_class=400)
    train_data = {'signals': train_signals, 'labels': train_labels}
    np.save(data_dir / 'diabetes_train.npy', train_data)
    print(f"Train set saved: {train_signals.shape}")
    
    # Validation set
    val_signals, val_labels = generate_dataset(n_samples_per_class=100)
    val_data = {'signals': val_signals, 'labels': val_labels}
    np.save(data_dir / 'diabetes_val.npy', val_data)
    print(f"Validation set saved: {val_signals.shape}")
    
    # Test set
    test_signals, test_labels = generate_dataset(n_samples_per_class=100)
    test_data = {'signals': test_signals, 'labels': test_labels}
    np.save(data_dir / 'diabetes_test.npy', test_data)
    print(f"Test set saved: {test_signals.shape}")
    
    print("\nSynthetic datasets generated successfully!")
    print(f"Location: {data_dir.absolute()}")


if __name__ == '__main__':
    main()
