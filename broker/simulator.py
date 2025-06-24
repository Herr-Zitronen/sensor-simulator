import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime
from datetime import timezone
import ssl

broker = "mosquitto"  
port = 1883
topic = "sensor/temperature"
client_id = f"sensor_{hex(random.getrandbits(24))[2:]}"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión: código: {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"Desconectado del broker MQTT. Código: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Configuración TLS
#context = ssl.create_default_context() 
#context.check_hostname = False
#context.verify_mode = ssl.CERT_NONE
#lient.tls_set_context(context)


try:
    client.connect(broker, port=port, keepalive=60)
    client.loop_start()

    while True:
        temperature = round(random.uniform(15, 35), 2)  # Temperatura aleatoria entre 15 y 35
        message = json.dumps({
            "temperature": temperature,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        # Publicar
        result = client.publish(topic, message, qos=1)
        status = result[0]
        if status == 0:
            print(f"Publicado en {topic}: {message}", flush=True)
        else:
            print(f"Error al publicar en el tópico {topic}")

        time.sleep(5)

# ctrl-c
except KeyboardInterrupt:
    print("Interrumpido por el usuario")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    client.loop_stop()
    client.disconnect()
    print("Cliente MQTT desconectado")