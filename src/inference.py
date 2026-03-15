"""
Inferencia en tiempo real desde sensores
"""
import torch
import numpy as np
import argparse
import serial
import time
from collections import deque

from data.preprocessing import SensorPreprocessor
from models.cnn1d import CNN1DClassifier, ResCNN1D
from models.transformer import SensorTransformer


class RealTimeSensorReader:
    """Lee datos de sensores en tiempo real"""
    
    def __init__(self, port, baudrate=9600, n_sensors=8, buffer_size=1000):
        self.serial = serial.Serial(port, baudrate)
        self.n_sensors = n_sensors
        self.buffer = deque(maxlen=buffer_size)
        
    def read_sample(self):
        """Lee una muestra de todos los sensores"""
        line = self.serial.readline().decode('utf-8').strip()
        values = [float(x) for x in line.split(',')]
        return np.array(values[:self.n_sensors])
    
    def collect_window(self, window_size=1000):
        """Recolecta una ventana de datos"""
        data = []
        for _ in range(window_size):
            sample = self.read_sample()
            data.append(sample)
            time.sleep(0.01)  # 100 Hz sampling
        return np.array(data).T  # (n_sensors, window_size)


class DiseasePredictor:
    """Predictor de enfermedades en tiempo real"""
    
    def __init__(self, model_path, device='cpu'):
        self.device = torch.device(device)
        
        # Cargar modelo
        checkpoint = torch.load(model_path, map_location=self.device)
        config = checkpoint['config']
        
        model_type = config['model']['type']
        if model_type == 'cnn1d':
            self.model = CNN1DClassifier(
                n_sensors=config['model']['n_sensors'],
                signal_length=config['model']['signal_length'],
                n_classes=config['model']['n_classes']
            )
        elif model_type == 'rescnn1d':
            self.model = ResCNN1D(
                n_sensors=config['model']['n_sensors'],
                signal_length=config['model']['signal_length'],
                n_classes=config['model']['n_classes']
            )
        elif model_type == 'transformer':
            self.model = SensorTransformer(
                n_sensors=config['model']['n_sensors'],
                signal_length=config['model']['signal_length'],
                n_classes=config['model']['n_classes']
            )
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        self.class_names = config.get('class_names', [f'Class_{i}' for i in range(config['model']['n_classes'])])
        self.preprocessor = SensorPreprocessor()
        
    def predict(self, sensor_data):
        """
        Predice enfermedad desde datos de sensores
        
        Args:
            sensor_data: numpy array (n_sensors, signal_length)
        
        Returns:
            predicted_class, confidence, all_probabilities
        """
        # Preprocesar
        processed = self.preprocessor.process_sensor_array(sensor_data)
        
        # Convertir a tensor
        tensor = torch.FloatTensor(processed).unsqueeze(0).to(self.device)
        
        # Predecir
        with torch.no_grad():
            output = self.model(tensor)
            probs = torch.softmax(output, dim=1)
            confidence, predicted = probs.max(1)
        
        predicted_class = self.class_names[predicted.item()]
        confidence_value = confidence.item()
        all_probs = probs.cpu().numpy()[0]
        
        return predicted_class, confidence_value, all_probs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, help='Path to model checkpoint')
    parser.add_argument('--sensor-port', type=str, default='COM3', help='Serial port for sensors')
    parser.add_argument('--baudrate', type=int, default=9600)
    parser.add_argument('--n-sensors', type=int, default=8)
    parser.add_argument('--window-size', type=int, default=1000)
    args = parser.parse_args()
    
    # Inicializar predictor
    predictor = DiseasePredictor(args.model)
    
    # Inicializar lector de sensores
    sensor_reader = RealTimeSensorReader(
        args.sensor_port,
        baudrate=args.baudrate,
        n_sensors=args.n_sensors
    )
    
    print("Sistema de diagnóstico iniciado. Presione Ctrl+C para detener.")
    print("-" * 60)
    
    try:
        while True:
            # Recolectar ventana de datos
            print("\nRecolectando datos de sensores...")
            sensor_data = sensor_reader.collect_window(args.window_size)
            
            # Predecir
            predicted_class, confidence, all_probs = predictor.predict(sensor_data)
            
            # Mostrar resultados
            print(f"\n{'='*60}")
            print(f"DIAGNÓSTICO: {predicted_class}")
            print(f"CONFIANZA: {confidence*100:.2f}%")
            print(f"{'='*60}")
            print("\nProbabilidades por clase:")
            for i, class_name in enumerate(predictor.class_names):
                print(f"  {class_name}: {all_probs[i]*100:.2f}%")
            
            # Esperar antes de siguiente lectura
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\nSistema detenido.")
        sensor_reader.serial.close()


if __name__ == '__main__':
    main()
