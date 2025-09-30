# simulator.py
import paho.mqtt.client as mqtt
import time, math, json, random

MQTT_BROKER = "localhost"
TOPIC = "sim/pzem"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

t = 0.0
freq = 50.0  # mains frequency for realism
while True:
    # Base sinusoidal RMS voltage & current plus small fluctuations
    Vrms = 230 + random.gauss(0, 0.8)  # small voltage noise
    Irms = 2.0 + 0.2*math.sin(t/10.0) + random.gauss(0, 0.02)
    # Power factor varying slowly between 0.85 and 0.99
    pf = 0.9 + 0.09*math.sin(t/60.0) + random.gauss(0, 0.005)
    P = Vrms * Irms * pf
    S = Vrms * Irms
    Q = math.sqrt(max(0.0, S*S - P*P))

    # Occasional transient or appliance start
    if random.random() < 0.02:
        # transient spike
        Irms += random.uniform(3.0, 6.0)
        P = Vrms * Irms * pf
        S = Vrms * Irms
        Q = math.sqrt(max(0.0, S*S - P*P))

    payload = {
        "timestamp": int(time.time()*1000),
        "V": round(Vrms, 2),
        "I": round(Irms, 3),
        "P": round(P, 2),
        "Q": round(Q, 2),
        "S": round(S, 2),
        "pf": round(pf, 3)
    }
    client.publish(TOPIC, json.dumps(payload), qos=0, retain=False)
    t += 1
    time.sleep(1)  # publish every second
