#ifndef CONEXAO_H
#define CONEXAO_H

#include <WiFi.h>
#include <PubSubClient.h>

const char* SSID_WIFI = "WIFI-IOT";
const char* SENHA_WIFI = "Ac5ce1ss0@IOT";


const char* BROKER_MQTT = "broker.hivemq.com";
const int PORTA_MQTT = 1883;
const char* TOPICO_MQTT = "casa/sala/iluminacao";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

void conectarWiFi() {
  Serial.print("Conectando ao Wi-Fi: ");
  Serial.println(SSID_WIFI);
  WiFi.begin(SSID_WIFI, SENHA_WIFI);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Conectado!");
}

void reconectarMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Tentando conectar ao Broker MQTT...");
    String clientId = "ESP32_PIR_Client_";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println(" Conectado ao MQTT!");
    } else {
      Serial.print(" Falhou. Código de erro: ");
      Serial.print(mqttClient.state());
      Serial.println(" Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

void setupConexao() {
  conectarWiFi();
  mqttClient.setServer(BROKER_MQTT, PORTA_MQTT);
}


void loopConexao() {
  if (!mqttClient.connected()) {
    reconectarMQTT();
  }
  mqttClient.loop();
}

void enviarEventoMQTT(String statusLuz, String evento) {
  if (mqttClient.connected()) {
    String payload = "{\"comodo\":\"Sala\", \"status_luz\":\"" + statusLuz + "\", \"evento\":\"" + evento + "\"}";
    
    mqttClient.publish(TOPICO_MQTT, payload.c_str());
    Serial.print("[MQTT ENVIADO]: ");
    Serial.println(payload);
  }
}

#endif