#include <WiFi.h>
#include <HTTPClient.h>

const int PINO_PIR = 13;   
const int PINO_LED = 12;   

// Substitua pela URL exata da sua Vercel
const char* URL_VERCEL = "https://SEU-PROJETO.vercel.app/api/evento";

int estadoAnteriorPIR = LOW;
unsigned long ultimoTempoMovimento = 0;
const long tempoEspera = 1000; // Reduzido para 1 segundo para maior agilidade

void enviarEventoHTTP(String statusLuz, String evento) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(URL_VERCEL);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"comodo\":\"Sala\", \"status_luz\":\"" + statusLuz + "\", \"evento\":\"" + evento + "\"}";

    // Envia o POST imediatamente
    int httpCode = http.POST(jsonPayload);
    http.end(); // Fecha a porta para estar pronto para a próxima
  }
}

void loop() {
  int movimentoAtual = digitalRead(PINO_PIR);

  // Assim que o pino mudar de LOW para HIGH, dispara na mesma hora
  if (movimentoAtual != estadoAnteriorPIR && (millis() - ultimoTempoMovimento > tempoEspera)) {
    if (movimentoAtual == HIGH) {
      digitalWrite(PINO_LED, HIGH);
      enviarEventoHTTP("Acesa", "Movimento Detectado");
    } else {
      digitalWrite(PINO_LED, LOW);
      enviarEventoHTTP("Apagada", "Movimento Cessou");
    }
    
    estadoAnteriorPIR = movimentoAtual;
    ultimoTempoMovimento = millis();
  }
}