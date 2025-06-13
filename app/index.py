import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime
from datetime import timezone
import ssl

# Configuración del cliente MQTT
broker = "broker"  
port = 8883
topic = "sensor/temperature"
client_id = f"sensor_{hex(random.getrandbits(24))[2:]}"

# Función que se llama al conectar exitosamente
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión: código {reason_code}")

# Función que se llama en caso de desconexión
def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"Desconectado del broker MQTT. Código: {reason_code}")

# Crear cliente y asignar callbacks
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Configuración de TLS
client.tls_set(
    ca_certs=None,  # Reemplazar con la ruta al certificado CA si es necesario
    certfile=None,  # Reemplazar con la ruta al certificado del cliente si es necesario
    keyfile=None,   # Reemplazar con la ruta a la clave del cliente si es necesario
    tls_version=ssl.PROTOCOL_TLSv1_2,  # Usar TLS 1.2 o superior
    ciphers=None
)
client.tls_insecure_set(False)  # Validar el certificado del servidor

# Conectar al broker
try:
    client.connect(broker, port=port, keepalive=60)
    client.loop_start()  # Inicia el bucle de red en segundo plano

    while True:
        temperature = round(random.uniform(15, 35), 2)  # Temperatura aleatoria entre 15 y 35
        message = json.dumps({
            "temperature": temperature,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        # Publicar el mensaje
        result = client.publish(topic, message, qos=1)
        status = result[0]
        if status == 0:
            print(f"Publicado en {topic}: {message}", flush=True)
        else:
            print(f"Error al publicar en el tópico {topic}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Interrumpido por el usuario")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    client.loop_stop()
    client.disconnect()
    print("Cliente MQTT desconectado")