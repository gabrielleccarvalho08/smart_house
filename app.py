import json
import os
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
from database import salvar_evento, get_db_connection

app = Flask(__name__)

def on_message(client, userdata, msg):
    try:
        dados = json.loads(msg.payload.decode())
        salvar_evento(dados.get('comodo'), dados.get('status_luz'), dados.get('evento'))
    except Exception as e:
        print(f"[MQTT ERRO]: {e}")

# O MQTT só roda em ambiente local, evitando travar a Vercel
if os.environ.get('VERCEL') is None:
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.connect("broker.hivemq.com", 1883, 60)
        mqtt_client.subscribe("casa/sala/iluminacao")
        mqtt_client.loop_start()
    except Exception as e:
        print(f"MQTT Desconectado: {e}")

@app.route('/api/evento', methods=['POST'])
def receber_evento():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Payload invalido"}), 400
    try:
        salvar_evento(dados.get('comodo'), dados.get('status_luz'), dados.get('evento'))
        return jsonify({"mensagem": "Evento registrado com sucesso!"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422

@app.route('/api/registros', methods=['GET'])
def listar_registros():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, comodo, status_luz, evento, data_hora FROM registros_iluminacao ORDER BY data_hora DESC LIMIT 20;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        resultados = [
            {"id": r[0], "comodo": r[1], "status_luz": r[2], "evento": r[3], "data_hora": str(r[4])}
            for r in rows
        ]
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)