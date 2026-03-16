/*
 * Lector de Sensores MQ para Nariz Electrónica
 * Compatible con Arduino Uno/Mega
 * 
 * Conexiones:
 * - MQ-2 (Gas inflamable) -> A0
 * - MQ-3 (Alcohol) -> A1
 * - MQ-4 (Metano) -> A2
 * - MQ-5 (GLP) -> A3
 * - MQ-6 (GLP/Butano) -> A4
 * - MQ-7 (CO) -> A5
 * - MQ-8 (H2) -> A6
 * - MQ-135 (Calidad aire) -> A7
 */

const int NUM_SENSORS = 8;
const int SENSOR_PINS[NUM_SENSORS] = {A0, A1, A2, A3, A4, A5, A6, A7};
const int SAMPLING_RATE = 100; // Hz
const int DELAY_MS = 1000 / SAMPLING_RATE;

// Calibración (ajustar según tu hardware)
const float R0[NUM_SENSORS] = {10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0};

void setup() {
  Serial.begin(9600);
  
  // Configurar pines como entrada
  for (int i = 0; i < NUM_SENSORS; i++) {
    pinMode(SENSOR_PINS[i], INPUT);
  }
  
  // Tiempo de calentamiento de sensores (2 minutos)
  Serial.println("Calentando sensores...");
  delay(120000);
  Serial.println("Listo para medir");
}

void loop() {
  // Leer todos los sensores
  for (int i = 0; i < NUM_SENSORS; i++) {
    int rawValue = analogRead(SENSOR_PINS[i]);
    
    // Convertir a voltaje (0-5V)
    float voltage = rawValue * (5.0 / 1023.0);
    
    // Calcular resistencia del sensor
    float Rs = ((5.0 * 10.0) / voltage) - 10.0;
    
    // Ratio Rs/R0
    float ratio = Rs / R0[i];
    
    // Enviar valor
    Serial.print(ratio);
    
    if (i < NUM_SENSORS - 1) {
      Serial.print(",");
    }
  }
  
  Serial.println();
  delay(DELAY_MS);
}
