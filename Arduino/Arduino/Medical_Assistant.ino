void setup() {
  pinMode(2, OUTPUT);   // Paracetamol
  pinMode(3, OUTPUT);   // Ibuprofen
  pinMode(4, OUTPUT);   // Antacid
  pinMode(5, OUTPUT);   // Cetirizine
  pinMode(7, OUTPUT);   // Eno
  pinMode(6, OUTPUT);   // Buzzer (SOS)

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();

    // Turn OFF all first
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    digitalWrite(7, LOW);
    digitalWrite(6, LOW);

    // Medicine LEDs
    if (data == '1') {
      digitalWrite(2, HIGH);   // Paracetamol
    }
    else if (data == '2') {
      digitalWrite(3, HIGH);   // Ibuprofen
    }
    else if (data == '3') {
      digitalWrite(4, HIGH);   // Antacid
    }
    else if (data == '4') {
      digitalWrite(5, HIGH);   // Cetirizine
    }
    else if (data == '5') {
      digitalWrite(7, HIGH);   // Eno
    }

    // 🚨 SOS / Emergency
    else if (data == 'S') {
      for (int i = 0; i < 6; i++) {
        digitalWrite(6, HIGH);
        delay(300);
        digitalWrite(6, LOW);
        delay(300);
      }
    }
  }
}
